# stdlib
import random
import time
import os

# 3rd party
from ddtrace import tracer
from flask import Response, jsonify, current_app
from flask import request as flask_request

# internal
from bootstrap import create_app, db
from models import Sensor

sensors = []

app = create_app()


@app.route('/')
def hello():
    return Response({'Hello from Sensors': 'world'}, mimetype='application/json')


@app.route('/sensors', methods=['GET', 'POST'])
def get_sensors():
    if flask_request.method == 'GET':
        app.logger.info('Fetching all sensors')
        sensors = Sensor.query.all()
        system_status = []
        time.sleep(0.2)  # add a sleep to simulate a request taking a little longer
        for sensor in sensors:
            system_status.append(sensor.serialize())
        app.logger.info(f'Sensors GET called with a total of {len(system_status)}')
        return jsonify({'sensor_count': len(system_status),
                        'system_status': system_status})
    elif flask_request.method == 'POST':
        app.logger.info('Adding a new sensor')
        sensors.append({'sensor_no': len(sensors) + 1, 'value': random.randint(1,100)})
        app.logger.info(f'Sensor number {len(sensors)} created')
        return jsonify(sensors)
    else:
        app.logger.warn(f'Unknown request method {flask_request.method}')
        err = jsonify({'error': 'Invalid request method'})
        err.status_code = 405
        return err


@app.route('/sensors/<id>/')
def sensor(id):
    app.logger.info(f'Getting info for sensor {id}')
    return jsonify(Sensor.query.get(id).serialize())


@app.route('/refresh_sensors')
def refresh_sensors():
    app.logger.info('Calling refresh sensor simulator')
    sensors = simulate_all_sensors()

    return jsonify({'sensor_count': len(sensors),
                    'system_status': sensors})


@tracer.wrap(name='sensor-simulator')
def simulate_all_sensors():
    app.logger.debug('Fetching all sensors')
    sensors = Sensor.query.all()

    app.logger.debug('Updating sensor values')
    for sensor in sensors:
        sensor.value = random.randint(1, 100)
    db.session.add_all(sensors)
    db.session.commit()
    app.logger.info('Sensor data updated')

    do_extra_work()

    return [s.serialize() for s in sensors]


def do_extra_work():
    if os.environ.get('WORKSHOP_ADD_LATENCY') != 'true':
        return

    # do extra work for these customers
    customer_id = flask_request.headers.get('x-customer-id')
    if customer_id in ('72618136', '1f86decd', 'aa4b5989'):
        current_app.logger.warn(f'Doing extra work for customer {customer_id}')
        db.session.execute('select pg_sleep(2);')

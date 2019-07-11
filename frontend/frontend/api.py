# stdlib
import os
import random
import subprocess

# 3rd party
from ddtrace import tracer
from flask import Flask, jsonify, send_from_directory
from flask import request as flask_request
from flask_cors import CORS
import requests

# internal
from .utils import get_user_id, maybe_raise_exception

app = Flask('api')

if os.environ['FLASK_DEBUG']:
    CORS(app)


@app.route('/')
def homepage():
    app.logger.info("Homepage called")
    return app.send_static_file('index.html')


@app.route('/status')
def system_status():
    status = requests.get('http://sensors:5002/sensors').json()
    app.logger.info(f"Sensor status: {status}")
    pumps = requests.get('http://pumps:5001/devices').json()
    users = requests.get('http://node:5004/users').json()
    return jsonify({'sensor_status': status, 'pump_status': pumps, 'users': users})


@app.route('/users', methods=['GET', 'POST'])
def users():
    if flask_request.method == 'POST':
        newUser = flask_request.get_json()
        app.logger.info(f"Adding new user: {newUser}")
        userStatus = requests.post('http://node:5004/users', json=newUser).json()
        return jsonify(userStatus)
    elif flask_request.method == 'GET':
        app.logger.info(f"Getting all users")
        users = requests.get('http://node:5004/users').json()
        return jsonify(users)


@app.route('/add_sensor')
def add_sensor():
    app.logger.info('Adding a new sensor')
    sensors = requests.post('http://sensors:5002/sensors').json()
    return jsonify(sensors)


@app.route('/add_pump', methods=['POST'])
def add_pump():
    pumps = requests.post('http://pumps:5001/devices').json()
    app.logger.info(f"Getting {pumps}")
    return jsonify(pumps)


@app.route('/generate_requests', methods=['POST'])
def call_generate_requests():
    payload = flask_request.get_json()
    span = tracer.current_root_span()
    span.set_tags({'requests': payload['total'], 'concurrent': payload['concurrent']})

    output = subprocess.check_output(['/app/traffic_generator.py',
                                      str(payload['concurrent']), 
                                      str(payload['total']),
                                      str(payload['url'])])
    app.logger.info(f"Result for subprocess call: {output}")
    return jsonify({'traffic': str(payload['concurrent']) + ' concurrent requests generated, ' + 
                               str(payload['total'])  + ' requests total.',
                    'url': payload['url']})


# generate requests for one user to see tagged
# enable user sampling because low request count
@app.route('/generate_requests_user')
def call_generate_requests_user():
    users = requests.get('http://node:5004/users').json()
    user = random.choice(users)
    span = tracer.current_root_span()
    span.set_tags({'user_id': user['id']})

    output = subprocess.check_output(['/app/traffic_generator.py',
                                     '20',
                                     '100',
                                     'http://node:5004/users/' + user['uid']])
    app.logger.info(f"Chose random user {user['name']} for requests: {output}")
    return jsonify({'random_user': user['name']})


@app.route('/simulate_sensors')
def simulate_sensors():
    app.logger.info('Simulating refresh of sensor data')
    sensors = requests.get('http://sensors:5002/refresh_sensors').json()
    return jsonify(sensors)


@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

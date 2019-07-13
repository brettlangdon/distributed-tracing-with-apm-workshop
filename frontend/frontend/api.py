# stdlib
import os

# 3rd party
from ddtrace import tracer
from flask import Flask, jsonify, send_from_directory
from flask import request as flask_request
from flask_cors import CORS
import requests

# internal
from .sensors import get_sensor_data
from .utils import get_customer_id, get_request_headers

app = Flask('api')

if os.environ['FLASK_DEBUG']:
    CORS(app)


@app.route('/simulate_sensors')
def simulate_sensors():
    sensors = get_sensor_data()
    return jsonify(sensors)


@app.route('/')
def homepage():
    return app.send_static_file('index.html')


@app.route('/status')
def system_status():
    status = requests.get('http://sensors:5002/sensors', headers=get_request_headers()).json()
    app.logger.info(f'Sensor status: {status}')
    pumps = requests.get('http://pumps:5001/devices', headers=get_request_headers()).json()
    users = requests.get('http://node:5004/users', headers=get_request_headers()).json()
    return jsonify({'sensor_status': status, 'pump_status': pumps, 'users': users})


@app.route('/users', methods=['GET', 'POST'])
def users():
    if flask_request.method == 'POST':
        newUser = flask_request.get_json()
        app.logger.info(f'Adding new user: {newUser}')
        userStatus = requests.post(
            'http://node:5004/users',
            json=newUser,
            headers=get_request_headers(),
        ).json()
        return jsonify(userStatus)
    elif flask_request.method == 'GET':
        app.logger.info(f'Getting all users')
        users = requests.get('http://node:5004/users', headers=get_request_headers()).json()
        return jsonify(users)


@app.route('/add_sensor')
def add_sensor():
    app.logger.info('Adding a new sensor')
    sensors = requests.post('http://sensors:5002/sensors', headers=get_request_headers()).json()
    return jsonify(sensors)


@app.route('/add_pump', methods=['POST'])
def add_pump():
    pumps = requests.post('http://pumps:5001/devices', headers=get_request_headers()).json()
    app.logger.info(f'Getting {pumps}')
    return jsonify(pumps)


@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(app.static_folder, path)

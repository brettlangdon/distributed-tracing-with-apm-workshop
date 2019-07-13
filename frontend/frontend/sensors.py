from flask import current_app
import requests

from .utils import get_customer_data, get_request_headers


def get_sensor_data():
    try:
        get_customer_data()
    except Exception:
        current_app.logger.exception('Failed to fetch customer data')
        # re-raise to cause an error
        raise

    current_app.logger.info('Simulating refresh of sensor data')
    resp = requests.get('http://sensors:5002/refresh_sensors', headers=get_request_headers())
    resp.raise_for_status()
    return resp.json()

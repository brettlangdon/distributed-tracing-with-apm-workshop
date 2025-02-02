from contextlib import contextmanager
import os

from ddtrace import tracer, patch; patch(sqlite3=True, psycopg=True)  # noqa
from flask import Flask
from models import Sensor, Network, db

# configure the tracer so that it reaches the Datadog Agent
# available in another container
tracer.configure(hostname='agent')

DB_USERNAME = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']


@contextmanager
def disable_tracer():
    try:
        tracer.enabled = False
        yield
    finally:
        tracer.enabled = True


def create_app():
    """Create a Flask application"""
    with disable_tracer():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + 'db/' + DB_USERNAME
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        initialize_database(app, db)
        return app


def initialize_database(app, db):
    """Drop and restore database in a consistent state"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        first_network = Network(name='First Network', site='DEL18DT')
        first_network.sensors.extend([Sensor(name='Bulkhead 5 Water Level', value=50),
                                      Sensor(name='Bulkhead 7 Water Level', value=20),
                                      Sensor(name='Bulkhead 2 Water Level', value=40)])
        second_network = Network(name='Second Network', site='DEL23DT')
        second_network.sensors.extend([Sensor(name='Rain Sensor Front Level', value=250),
                                       Sensor(name='Rain  Sensor Back Level', value=620)])
        db.session.add(first_network)
        db.session.add(second_network)
        db.session.commit()

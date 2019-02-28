from influxdb import InfluxDBClient
from flask import Blueprint
import os

influx_blueprint = Blueprint('Influxdb', __name__)
host = "localhost"
port = 8086
database = "waterflow"

host = 'localhost'

try:
    if os.environ["DEPLOY"]:
        host = os.environ["INFLUX_HOST"]
except Exception as e:
    print("Running on develop environment")

client = InfluxDBClient(host=host, port=port, database=database)


def get_measurements(dev_id, f, t):
    query = "SELECT * FROM flow WHERE dev_id='{}' AND time >= {} AND time <= {}".format(dev_id, f, t)
    print(query)
    results = client.query(query)
    points = results.get_points()
    measurements = []
    for point in points:
        measurements.append(point)
    return measurements

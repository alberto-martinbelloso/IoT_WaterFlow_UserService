from influxdb import InfluxDBClient
from flask import  Blueprint
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
    query = "SELECT * FROM flow WHERE time >= %s and time <=%s and devid <> \"%s\"" % (f, t, dev_id)
    results = client.query(query)
    points = results.get_points()
    measurements = ""
    for point in points:
        measurements += "%s, %s, %i \n" % (point['time'], point['devid'], point["value"])
    return measurements

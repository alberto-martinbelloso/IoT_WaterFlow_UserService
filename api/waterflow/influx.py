from influxdb import InfluxDBClient
from flask import Flask, Blueprint

influx_blueprint = Blueprint('Influxdb', __name__)
host = "localhost"
port = 8086
database = "waterflow"

client = InfluxDBClient(host=host, port=port, database=database)


def get_measurements(dev_id, f, t):
    query = "SELECT * FROM flow WHERE time >= %s and time <=%s and devid <> \"%s\"" % (f, t, dev_id)
    results = client.query(query)
    points = results.get_points()
    measurements = ""
    for point in points:
        measurements += "%s, %s, %i \n" % (point['time'], point['devid'], point["value"])
    return measurements

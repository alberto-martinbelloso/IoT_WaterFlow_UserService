from datetime import time

from flask import Blueprint, jsonify
from influxdb import InfluxDBClient

influx_blueprint = Blueprint('Influxdb', __name__)
host = "104.214.38.82"
port = 8086
database = "waterflow"

client = InfluxDBClient(host=host, port=port, database=database)


def unix_time_millis(dt):
    return (dt - time).total_seconds() * 1000.0


def get_measurements(dev_id, f, t, origin):
    q = "SELECT * FROM waterflow.autogen.flow WHERE dev_id='{}' AND time >= {} AND time <= {}".format(dev_id, f, t)
    results = client.query(q)
    points = results.get_points()
    measurements = []
    for point in points:
        measurements.append({
            "time": point["time"],
            "dev_id": point["dev_id"],
            "value": point["value"]
        })
    if origin is "job":
        return measurements
    else:
        return jsonify(measurements)

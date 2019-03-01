from influxdb import InfluxDBClient
from flask import jsonify
import os

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


def get_measurements(dev_id, f, t, origin=""):
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

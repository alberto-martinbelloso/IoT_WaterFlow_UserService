from flask import jsonify
from api.influx import client


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

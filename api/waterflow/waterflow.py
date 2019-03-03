from api.influx import client


def get_measurements(dev_id, f, t, group, origin=""):
    k = 'value'
    if group is None:
        q = "SELECT * FROM waterflow WHERE dev_id='{}' AND time >= {} AND time <= {}".format(dev_id, f, t)
    else:
        q = "SELECT sum(value) as sum FROM waterflow WHERE dev_id='{}' AND time >= {} AND time <= {} GROUP BY time({})".format(
            dev_id, f, t, group)
        k = 'sum'
    results = client.query(q)
    points = results.get_points()
    measurements = []
    for point in points:
        measurements.append({
            "time": point["time"],
            "dev_id": dev_id,
            "value": point[k]
        })
    return measurements

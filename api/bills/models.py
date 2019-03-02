class Bill(object):
    def __init__(self, user, from_date, to_date):
        self.user_id = user.id
        self.username = user.username
        self.from_date = from_date
        self.to_date = to_date
        self.devices = user.devices
        self.measurements = dict()
        self.waterflow = 0
        self.price = 0

    def fill_measurements(self, dev_id, measurements):
        if id not in self.measurements:
            self.measurements[dev_id] = []
        for measurement in measurements:
            self.measurements[dev_id].append({
                "value": measurement["value"],
                "time": measurement["time"],
            })


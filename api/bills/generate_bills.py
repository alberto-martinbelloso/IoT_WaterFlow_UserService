import datetime
import calendar

from api import User
from api.mongo import db
from api.waterflow.influx import get_measurements


def job():
    today = datetime.date.today()
    last_day = datetime.date.fromtimestamp(1551350759)  # 28 Feb
    if calendar.monthrange(today.year, today.month)[1] == today.day:
        first_day = datetime.date.today().replace(day=1)
        generate_bill(first_day, today)
    print("passing")


def generate_bill(from_day, to_day):
    f = calendar.timegm(from_day.timetuple()) * 1000000000
    t = calendar.timegm(to_day.timetuple()) * 1000000000
    collection = db['users']
    users = collection.find({})

    for user in users:
        u = User(user)
        bill = Bill(u, from_day, to_day)

        for device in u.devices:
            measurements = get_measurements(device, f, t, "job")
            bill.fill_measurements(device, measurements)

            total = 0
            for m in measurements:
                total += m["value"]

            bill.waterflow = total
            bill.price = total * 0.015

            insert_json = {
                "username": bill.username,
                "date": bill.to_date.strftime("%Y-%m-%d"),
                "waterflow": bill.waterflow,
                "price": bill.price
            }

            db.bills.insert(insert_json)


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


import datetime
import calendar

from api import User
from api.bills.models import Bill
from api.mongo import db
from api.waterflow.waterflow import get_measurements


def job():
    print("INFO | Running job")
    today = datetime.date.today()
    # last_day = datetime.date.fromtimestamp(1551350759)  # 28 Feb
    if calendar.monthrange(today.year, today.month)[1] == today.day:
        first_day = datetime.date.today().replace(day=1)
        generate_bill(first_day, today)


def generate_bill(from_day, to_day):
    f = calendar.timegm(from_day.timetuple()) * 1000000000
    t = calendar.timegm(to_day.timetuple()) * 1000000000
    users = db['users'].find({})
    prices = db['price'].find().sort([('timestamp', -1)]).limit(1)
    price = prices[0]['price']

    for user in users:
        u = User(user)
        bill = Bill(u, from_day, to_day)

        for device in u.devices:
            measurements = get_measurements(device, f, t, None, "job")
            bill.fill_measurements(device, measurements)

            total = 0
            for m in measurements:
                total += m["value"]

            bill.waterflow = total
            bill.price = total * price

            insert_json = {
                "username": bill.username,
                "date": bill.to_date.strftime("%Y-%m-%d"),
                "waterflow": bill.waterflow,
                "import": bill.price,
                "price": price
            }

            db['bills'].insert(insert_json)

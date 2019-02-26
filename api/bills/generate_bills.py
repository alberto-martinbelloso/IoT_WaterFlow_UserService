import datetime
import calendar


def job():
    today = datetime.date.today()
    tomorrow = datetime.date.fromtimestamp(1551350759)  # 28 Feb
    tomorrow = datetime.date.fromtimestamp(1554029159)  # 31 Mar
    if calendar.monthrange(today.year, today.month)[1] != today.day:
        print(today, "not last day of month")
    if calendar.monthrange(tomorrow.year, tomorrow.month)[1] == tomorrow.day:
        print(tomorrow, "last day of month")
        generate_bill()


def generate_bill():
    pass

from api import app
from api.bills.generate_bills import job
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


with app.app_context():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=job, trigger="interval", hours=12)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

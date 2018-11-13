from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from flask import Flask
from flask_bootstrap import Bootstrap
from SpeedTester import SpeedTester

app = Flask(__name__)
Bootstrap(app)

speed_tester = SpeedTester()
scheduler = BackgroundScheduler()
scheduler.add_job(func=speed_tester.run_speed_test, trigger="interval", minutes=15)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

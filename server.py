from flask import Flask
from flask_bootstrap import Bootstrap
import speedtest

app = Flask(__name__)
Bootstrap(app)
st = speedtest.Speedtest()


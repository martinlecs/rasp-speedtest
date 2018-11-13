from flask import Flask
import speedtest

app = Flask(__name__)
st = speedtest.Speedtest()


from server import app
from flask import render_template
from server import speed_tester


@app.route('/')
def index():
    data = speed_tester.get_results()
    return render_template('index.html', data=data)

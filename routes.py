from flask import render_template
import globals
from server import app
from server import speed_tester
import sqlite3

@app.route('/')
def index():
    with sqlite3.connect(globals.DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM results')
        data = c.fetchall()
    return render_template('index.html', data=data)

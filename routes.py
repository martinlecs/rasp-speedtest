from server import app
from flask import render_template


@app.route('/')
def index():
    # polls database for changes and displays changes
    return 'Hello World'

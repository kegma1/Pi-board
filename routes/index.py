from __main__ import app
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html", title="Heia")
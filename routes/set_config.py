from __main__ import app, config_set
import state
from flask import render_template, request

@app.route('/set_stop', methods = ["POST"])
def set_stop():
    data = request.get_json()
    print(data["stop_id"])

    state.stop_id = data["stop_id"]
    config_set.set()
    return "", 204
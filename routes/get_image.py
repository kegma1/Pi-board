from __main__ import app, playlist, current_app

@app.route('/get_current_image')
def get_current_image():
    return playlist[current_app].get_image()


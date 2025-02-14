# set up logging
import os, logging.config
logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'config', 'logging.conf'))

# suppress warning from inky library https://github.com/pimoroni/inky/issues/205
import warnings
warnings.filterwarnings("ignore", message=".*Busy Wait: Held high.*")

from PIL import Image, ImageDraw, ImageFont
import os
import logging
import threading
from time import sleep
from flask import Flask
## 800 x 480 
logger = logging.getLogger(__name__)
logger.info("Starting web server")

app = Flask(__name__)

import routes.index


def main():
    while True:
        img = Image.new("RGBA", (800, 480), (255, 255, 255, 255))
        d = ImageDraw.Draw(img)

        d.text((10, 10), "Hello", fill=(255, 255, 255, 128))

        img.show()
        sleep(80)

if __name__ == "__main__":
    from werkzeug.serving import is_running_from_reloader

    app.run()

        
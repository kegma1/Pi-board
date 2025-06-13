# suppress warning from inky library https://github.com/pimoroni/inky/issues/205
# import warnings
# warnings.filterwarnings("ignore", message=".*Busy Wait: Held high.*")

import datetime
from PIL import Image
import threading
import time
from flask import Flask, url_for
import requests
from libs.colors import WHITE
import sys

from Apps.TestApp.TestApp import TestApp

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO

## 800 x 480 

app = Flask(__name__)
playlist = [TestApp()]
current_app = 0

width, height = 800, 480

import routes.index
import routes.get_image

# img = Image.new("RGB", (800, 480), WHITE)

display = None

def take_screenshot_as_pillow_image(route, width, height):
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(route)

        driver.execute_cdp_cmd(
            "Emulation.setDeviceMetricsOverride",
            {
                "mobile": False,
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
            },
        )
        
        image_data = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(image_data))
        return image
    finally:
        driver.quit()

def wait_for_server(url, timeout=30):
    start_timer = time.time()
    while time.time() - start_timer < timeout:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                print("Flask server is ready")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    raise RuntimeError("Flask server did not start in time.")

def main():

    while True:
        img = take_screenshot_as_pillow_image("http://localhost:3000/get_current_image", display.width, display.height)
        display.set_image(img)
        display.show()

        seconds_to_min = 60 - datetime.datetime.now(datetime.timezone.utc).second
        time.sleep(seconds_to_min)

def run_server():
    app.run(port=3000, debug=True, use_reloader=False, threaded=True)

if __name__ == "__main__":
    if sys.argv[1] == "--dev":
        from inky.mock import InkyMockImpression
        display = InkyMockImpression((width, height))
    elif sys.argv[1] == "--release":
        from inky.auto import auto
        display = auto()
    else:
        print("ERROR: Wrong arguments")
        sys.exit(1)

    web_server_thread = threading.Thread(target=run_server, daemon=True)
    web_server_thread.start()

    wait_for_server("http://localhost:3000/")
    
    main()
        
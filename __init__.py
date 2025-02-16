# suppress warning from inky library https://github.com/pimoroni/inky/issues/205
# import warnings
# warnings.filterwarnings("ignore", message=".*Busy Wait: Held high.*")

from PIL import Image, ImageDraw, ImageFont
import os
import threading
from time import sleep
from flask import Flask
from libs.board import DepartureBoard
from libs.colors import WHITE
## 800 x 480 

app = Flask(__name__)

import routes.index

img = Image.new("RGB", (800, 480), WHITE)

boards = [DepartureBoard(img, "NSR:StopPlace:49662"), # Rådhuset   - buss
          DepartureBoard(img, "NSR:StopPlace:6488"),  # Grønnland  - metro
          DepartureBoard(img, "NSR:StopPlace:48048"), # skarberget - ferge
          DepartureBoard(img, "NSR:StopPlace:58382"), # akerbrygge - trikk og ferge
          DepartureBoard(img, "NSR:StopPlace:58404"), # Nationaltheatret - trikk, ferge, metro og buss
          ]
selected_board = 4

def main():
    # while True:
    boards[selected_board].draw_board()
    img.show()
    sleep(60)

def run_server():
    app.run(port=3000, debug=True, use_reloader=False, threaded=True)

if __name__ == "__main__":
    web_server_thread = threading.Thread(target=run_server, daemon=True)
    web_server_thread.start()
    
    main()
        
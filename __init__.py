# suppress warning from inky library https://github.com/pimoroni/inky/issues/205
# import warnings
# warnings.filterwarnings("ignore", message=".*Busy Wait: Held high.*")

from PIL import Image
import threading
from time import sleep
from flask import Flask
from boards.departureBoard import DepartureBoard
from boards.qrBoard import QRBoard
from libs.colors import WHITE
from inky.mock import InkyMockImpression
import sys
import socket
import state
## 800 x 480 

DEBUG = False
PORT = 6969

app = Flask(__name__)
config_set = threading.Event()

import routes.index
import routes.set_config

img = Image.new("RGB", (800, 480), WHITE)

display = None


# boards = [DepartureBoard(img, "NSR:StopPlace:49662"), # Rådhuset   - buss
#           DepartureBoard(img, "NSR:StopPlace:6488"),  # Grønland  - metro
#           DepartureBoard(img, "NSR:StopPlace:48048"), # skarberget - ferge
#           DepartureBoard(img, "NSR:StopPlace:58382"), # akerbrygge - trikk og ferge
#           DepartureBoard(img, "NSR:StopPlace:58404"), # Nationaltheatret - trikk, ferge, metro og buss
#           DepartureBoard(img, "NSR:StopPlace:59281"), # Harstad/Narvik lufthavn, Evenes - buss og fly
#           DepartureBoard(img, "NSR:StopPlace:58211"), # Oslo lufthavn - buss, fly og tåg
#           DepartureBoard(img, "NSR:StopPlace:62558"), # Narvikfjellet - ingen buss 😢
#           DepartureBoard(img, "NSR:StopPlace:58066"), # Fløibanen - gondol
#           ]
# selected_board = 0


def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def main():
    if state.stop_id is None:
        hostname = socket.gethostname()
        ip_addr = get_lan_ip()

        board = QRBoard(img, ip_addr, hostname, PORT)
        board.draw_board()

        display.set_image(img)
        display.show()
        config_set.wait()
    

    while True:
        config_set.clear()
        board = DepartureBoard(img, state.stop_id)
        board.draw_board()
        display.set_image(img)
        display.show()

        config_set.wait()


def run_server():
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG, use_reloader=False, threaded=True)

if __name__ == "__main__":
    if sys.argv[1] == "--dev":
        from inky.mock import InkyMockImpression
        display = InkyMockImpression((800, 480))

        DEBUG = True
    elif sys.argv[1] == "--release":
        from inky.auto import auto
        display = auto()
    else:
        print("ERROR: Wrong arguments")
        sys.exit(1)

    web_server_thread = threading.Thread(target=run_server, daemon=True)
    web_server_thread.start()

    
    main()
        
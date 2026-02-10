from boards.board import Board
from PIL import ImageFont, Image


import qrcode

fnt = ImageFont.truetype("./static/font/Kodchasan-Regular.ttf", 20)

background = (217, 242, 255)
fill = (48, 25, 52)


class QRBoard(Board):
    def __init__(self, img, ip_addr, hostname, port):
        super().__init__(img)
        self.ip_addr = ip_addr
        self.hostname = hostname
        self.port = port

    def draw_board(self):
        url = f"http://{self.ip_addr}:{self.port}"
        width, _ = self.img.size

        qr_offset = 50

        QRcode = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=10,
            border=0,
            )
        QRcode.add_data(url)
        QRcode.make(fit=True)

        qr = QRcode.make_image(fill_color = fill, back_color=background).convert('RGB')
        qr_w, qr_h = qr.size

        self.img.paste(qr, (int((width/2) - (qr_w/2)), qr_offset))
        url_len = self.d.textlength(url, fnt)

        self.d.text(((width/2) - (url_len/2), qr_h+qr_offset+10), url, fill=fill, font=fnt)


from PIL import ImageDraw

class Board:
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(self.img)

    def draw_board(self):
        pass


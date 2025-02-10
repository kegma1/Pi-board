from PIL import Image, ImageDraw, ImageFont
from time import sleep

## 800 x 480 


def main():
    img = Image.new("RGBA", (800, 480), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)

    d.text((10, 10), "Hello", fill=(255, 255, 255, 128))

    img.show()

if __name__ == "__main__":
    while True:
        main()
        sleep(80)
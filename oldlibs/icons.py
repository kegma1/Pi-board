from PIL import Image
import os
import glob

large_icons = {}
small_icons = {}

for filename in glob.glob("./static/icon/large/*.png"):
    im = Image.open(filename)
    large_icons[os.path.basename(filename)] = im

for filename in glob.glob("./static/icon/small/*.png"):
    im = Image.open(filename)
    small_icons[os.path.basename(filename)] = im

def mode_to_icon(mode, is_large = True):
    if is_large:
        match mode:
            case "air":
                return large_icons["Plane.png"]
            case "bus" | "trolleybus" |  "coach":
                return large_icons["Bus.png"]
            case "tram":
                return large_icons["Tram.png"]
            case "water":
                return large_icons["Ferry.png"]
            case "rail":
                return large_icons["Train.png"]
            case "metro":
                return large_icons["Metro.png"]
            case "lift" |"cableway":
                return large_icons["Cableway.png"]
            case "funicular":
                return large_icons["Funicular.png"]
            case _:
                return large_icons["Question.png"]
    else:
        match mode:
            case "air":
                return small_icons["Plane.png"]
            case "bus" | "trolleybus" |  "coach":
                return small_icons["Bus.png"]
            case "tram":
                return small_icons["Tram.png"]
            case "water":
                return small_icons["Ferry.png"]
            case "rail":
                return small_icons["Train.png"]
            case "metro":
                return small_icons["Metro.png"]
            case "lift" |"cableway":
                return small_icons["Cableway.png"]
            case "funicular":
                return small_icons["Funicular.png"]
            case _:
                return small_icons["Question.png"]

    
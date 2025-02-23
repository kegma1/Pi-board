BLACK = (0, 0, 0)           # #000000
WHITE = (217, 242, 255)     # #d9f2ff
GREEN = (3, 124, 76)        # #037c4c
BLUE = (27, 46, 198)        # #1b2ec6
RED = (245, 80, 34)         # #f55022
YELLOW = (255, 255, 68)     # #ffff44
ORANGE = (239, 121, 44)     # #ef792c
CLEAN = (255, 255, 255)     # #ffffff

# BLACK = (0, 0, 0)           # #000000
# WHITE = (255, 255, 255)     # #d9f2ff
# GREEN = (0, 255, 0)        # #037c4c
# BLUE = (0, 0, 255)        # #1b2ec6
# RED = (255, 0, 0)         # #f55022
# YELLOW = (255, 255, 0)     # #ffff44
# ORANGE = (255, 140, 0)     # #ef792c
# CLEAN = (255, 255, 255)     # #ffffff


# ferge og tog = blå
# metro = rød
# buss og annet = sort
# fly = grønn
# trikk = gul
# gondol og Kabelbane = oranjs

def mode_to_color(mode):
    match mode:
        case "air":
            return (GREEN, WHITE)
        case "bus" | "trolleybus" |  "coach":
            return (BLACK, WHITE)
        case "tram":
            return (YELLOW, BLACK)
        case "water" | "rail":
            return (BLUE, WHITE)
        case "metro":
            return (RED, WHITE)
        case "lift" | "funicular" | "cableway":
            return (ORANGE, WHITE)
        case _:
            return (BLACK, WHITE)
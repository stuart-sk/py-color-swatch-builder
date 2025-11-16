from colorsys import hsv_to_rgb
from math import cos, sin, radians

if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0][:-4])

from src.Types import SwatchColor

def get_color_rel_xy(color: SwatchColor, size: int):
    saturation = color.saturation * size // 100
    value = size - color.value * size//100
    return (saturation, value)

def get_hue_rotation_xy(color: SwatchColor, radius: int):
    # -150 to match CSP.
    degree = color.hue -150
    x = int(cos(radians(degree)) * radius)
    y = int(sin(radians(degree)) * radius)
    return (x,y)






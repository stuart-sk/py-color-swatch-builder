if __name__ == "__main__":
    import sys
    sys.path.insert(1, "E:/Code/py-color-swatch-builder")

from colorsys import rgb_to_hsv, hsv_to_rgb
from PIL import ImageColor

class SwatchColor:
    def __init__(self, rgb :tuple|str = "black"):
        if isinstance(rgb, tuple):
            self.rgb = rgb
        else:
            self.rgb = ImageColor.getrgb(rgb)
        self.hsv = rgb_to_hsv(*self.rgb)
        self.hue = int(self.hsv[0]*360)
        self.hue_rgb = tuple(int(x) for x in hsv_to_rgb(self.hsv[0], 1, 256))
        self.saturation = int(self.hsv[1]*100)
        self.value = int(self.hsv[2] /255 * 100)
    
    def __mul__(self, r):
        return SwatchColor(tuple(int(max(0,min(255,(x/255)*y))) for x, y in zip(self.rgb, r.rgb)))

    def __truediv__(self, r):
        return SwatchColor(tuple(x if y == 0 else int(max(0,min(255,(x*255)//y))) for x, y in zip(self.rgb, r.rgb)))
    
    def __str__(self):
        return f"{self.hue},{self.saturation},{self.value}"

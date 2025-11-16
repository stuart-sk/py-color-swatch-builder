if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0].split('src')[0])

    def main():
        img = Image.new("RGBA", (200,200), color="white")
        draw=ImageDraw.Draw(img)
        dot=ColorDot()
        dot.draw(draw,(10,10))
        dot.draw(draw,(50,30), SwatchColor("red"))
        dot.radius=20
        dot.border_width = 10
        dot.draw(draw,(50,30), SwatchColor("red"), SwatchColor("purple"))
        dot.draw(draw,(130,30), SwatchColor("red"), SwatchColor("purple"), 80)
        img.show()

from dataclasses import dataclass, field
from PIL import Image, ImageDraw
from src.Color import SwatchColor
from colorsys import hsv_to_rgb
import numpy as np

@dataclass
class ColorDot:
    def __init__(self, radius: int = 10, fill: SwatchColor = SwatchColor("white"), border_color: SwatchColor = SwatchColor(), border_width: int = 2):
        self.radius=radius
        self.fill = fill
        self.border_color = border_color
        self.border_width = border_width

    def draw(self, draw: ImageDraw.ImageDraw, xy: tuple[int,int], fill_override: SwatchColor = None, border_override: SwatchColor= None, radius_override: int = None ):
        radius = radius_override if radius_override else self.radius
        border_color = self.border_color if not border_override else border_override
        fill_color = self.fill if not fill_override else fill_override
        if self.border_width > 0:
            draw.circle(xy, radius, border_color.rgb)
        draw.circle(xy, radius-self.border_width, fill_color.rgb)

if __name__ == "__main__":
    main()
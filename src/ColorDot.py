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
        img.show()

from dataclasses import dataclass, field
from PIL import Image, ImageDraw
from src.Types import SwatchColor
from colorsys import hsv_to_rgb
import numpy as np

@dataclass
class ColorDot:
    radius: int = field(default=10)
    fill: SwatchColor = field(default=SwatchColor((255,255,255)))
    border_color: SwatchColor = field(default=SwatchColor((0,0,0)))
    border_width: int = field(default=2)

    def draw(self, draw: ImageDraw.ImageDraw, xy: tuple[int,int], fill_override: SwatchColor = None, border_override: SwatchColor= None):
        if self.border_width > 0:
            border_color = self.border_color if not border_override else border_override
            draw.circle(xy, self.radius, border_color.rgb)
        fill_color = self.fill if not fill_override else fill_override
        draw.circle(xy, self.radius-self.border_width, fill_color.rgb)

if __name__ == "__main__":
    main()
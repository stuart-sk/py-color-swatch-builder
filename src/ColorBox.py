#
# A tool to create Clip Studio Paint styled Hue/Saturation boxes
#

if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0].split('src')[0])
    def main():
        image = Image.new("RGBA", (500,500))
        draw = ImageDraw.Draw(image)
        color = Rgb("orange")
        color_box = ColorBox(300, color)
        dest = (30,30)
        color_box.paste_into(image, dest)
        color_box.draw_dot(draw, dest, ["red", "lightpink", "moccasin", "brown"])
        image.show()




        # SatValBox(color).show()
        # SatValBox(color, fill_with_color=False).show()


from dataclasses import dataclass, field
import operator
from PIL import Image, ImageDraw
from src.Rgb import Rgb
from src.ColorDot import ColorDot
from colorsys import hsv_to_rgb
from src.Utils import get_color_rel_xy
import numpy as np

@dataclass
class ColorBox:
    size: int # Size of box excluding border
    hue: Rgb
    border: int = field(default=4)
    border_fill: Rgb = field(default=Rgb())
    dot: ColorDot = field(default_factory=lambda: ColorDot())

    def __post_init__(self):
        self.box_size = self.size - 2*self.border

    def paste_into(self, image: Image.Image, dest: tuple):
        box = Image.new ("RGBA", (self.size, self.size), color=self.border_fill.rgb)
        box.alpha_composite(SatValColor(self.box_size, self.hue), (self.border, self.border))
        image.alpha_composite(box, dest)

    def draw_dot(self, draw: ImageDraw.ImageDraw, dest: tuple, colors: list[Rgb], dot_size: int = None, use_hue = False, border_fill = None):
        if not isinstance(colors, list):
            colors = [colors]
        for color in reversed(colors):
            if not isinstance(color, Rgb):
                color = Rgb(color)
            rel_xy = get_color_rel_xy(color, self.box_size)

            x = dest[0]  + self.border + rel_xy[0]
            y = dest[1]  + self.border + rel_xy[1]
            rgb = Rgb(color.hue_rgb) if use_hue else color

            self.dot.draw(draw, (x,y), rgb, border_override= border_fill, radius_override=dot_size)

    def get_dot_point(self, color:Rgb, dest: tuple=(0,0)):
        rel_xy = get_color_rel_xy(color, self.box_size)
        x = dest[0]  + self.border + rel_xy[0]
        y = dest[1]  + self.border + rel_xy[1]
        return (x,y)

def SatValColor(size, swatch_color: Rgb) -> Image:

    # Use RGBA for alpha compositing later
    img = Image.new("RGBA", (size,size), color="white")
    hue = swatch_color.hsv[0]

    sat = np.linspace(0.0, 1.0,size)
    #val = np.linspace(0.0,255.0,size)
    val = np.linspace(255.0,0.0,size)
    draw = ImageDraw.Draw(img)
    for y in range(size):
        for x in range(size):
            draw.point((x,y), tuple(int(x) for x in hsv_to_rgb(hue, sat[x], val[y])))
    return img


def SatValBox(colors:Rgb, size =200, border = 4, point_size = 2, border_width =4, fill_with_color = True) -> Image:
    image = Image.new("RGBA", (size,size), color=(0,0,0,0))
    draw = ImageDraw.Draw(image)
    box_size = size - 2*border
    line_box_size = box_size + 2*border_width


    # draw outside line
    if border_width > border:
        border_width = border
    if border_width > 0:
        draw.rectangle((border-border_width, border-border_width, size-border+border_width, size-border+border_width), fill="black")

    if not isinstance(colors, list):
        colors = [colors]

    if fill_with_color:
        image.alpha_composite(SatValColor(box_size, colors[0]),(border,border))
    else:
        draw.rectangle((border, border, size-border, size-border), fill=(0,0,0,0))

    for color in reversed(colors):
        saturation = color.saturation * (size - 2*border) // 100
        value = (size - 2*border) - color.value * (size - 2*border)//100
        x = border + saturation
        y = border + value
        draw.circle((x,y), point_size, "black" )
        draw.circle((x,y), point_size-3, color.rgb )

    return image

if __name__ == "__main__":
    main()
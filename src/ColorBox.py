#
# A tool to create Clip Studio Paint styled Hue/Saturation boxes
#

if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0].split('src')[0])
    def main():
        color = SwatchColor((255,0,0))
        SatValBox(color).show()
        SatValBox(color, fill_with_color=False).show()


from PIL import Image, ImageDraw
from src.Types import SwatchColor
from colorsys import hsv_to_rgb
import numpy as np


def SatValColor(size, swatch_color: SwatchColor) -> Image:

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


def SatValBox(colors:SwatchColor, size =200, border = 4, point_size = 2, border_width =4, fill_with_color = True) -> Image:
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
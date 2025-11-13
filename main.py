# from src.ColorBox import *
# from src.ColorWheel import *
# from src.ColorWheelBox import *
from src import ColorBox
from src.Types import SwatchColor
from src.Swatch import SwatchMaker
from src.Utils import *
import src.ColorWheel as ColorWheel
from PIL import Image, ImageDraw
from math import sqrt, asin



def main():
    # print("Py Color Swatch Builder")
    # color = SwatchColor((1,2,3))
    # print(color)
    SwatchMaker(medium_swatch)

def medium_swatch(color_list:list[SwatchColor]):
    size = 800
    page_size = (size + size//2, size)
    ring_size = 400
    border = 50
    hole = 500
    midpoint = size//2
    image = Image.new("RGBA", page_size, "white")
    draw = ImageDraw.Draw(image)
    inner_square_size = int(sqrt(2)*(hole/2)) + 6
    inner_square_offset = (size - inner_square_size) //2
    border = 10
    # image.alpha_composite(ColorBox.SatValBox(color_list, inner_square_size,point_size=10,border=10, border_width=4),(inner_square_offset, inner_square_offset))
    image.alpha_composite(ColorBox.SatValBox([color_list[0]], inner_square_size,point_size=10,border=border, border_width=4,fill_with_color=True),(inner_square_offset, inner_square_offset))

    y_unit = size // (len(color_list) + 1)
    y_offset = y_unit //2
    x_offset = size + 50
    h_degree = color_list[0].hsv[0]
    h_offset = 1.0 / len(color_list)
    radius = 100

    for i in reversed(range(len(color_list))):
        color = color_list[i]
    #for color in reversed(color_list):
        hsv_rgb = tuple(int(x) for x in hsv_to_rgb(h_degree + i * h_offset, 1, 255))
        start = tuple( int(x + midpoint) for  x in get_hue_rotation_xy(color, (hole//2 + border)))
        end = tuple(int(x + inner_square_offset + border) for x in get_color_rel_xy(color, inner_square_size - border *2))
        draw.line((start+end), fill="black", width=6)
        draw.line((start+end), fill=hsv_rgb, width=4)





        y = y_offset + (i+.5) * y_unit
        theta = asin((midpoint-y)/(midpoint+200))
        x = midpoint + abs(cos(theta)) * (midpoint + 200)

        draw.line((end+(x,y)), fill="black", width=6)
        draw.line((end+(x,y)), fill=hsv_rgb, width=4)

        draw.circle((x,y), radius= radius, fill=hsv_rgb)
        draw.circle((x,y), radius= radius -10, fill=color.rgb)

    image.alpha_composite(ColorWheel.small_rainbow_pi(size,hole,color_list, use_sat_val=True), (0,0))


    # cos(x) = adjacent / hypotenuse
    # cos(x) = adjacent
    # x = acos(adjacent)


    

    #sin(theta) = oposite / hypotenuse



    for i in range(len(color_list)):
        color = color_list[i]

        y = y_offset + (i+.5) * y_unit
        theta = asin((midpoint-y)/(midpoint+200))
        x = midpoint + abs(cos(theta)) * (midpoint + 200)
        hsv_rgb = tuple(int(x) for x in hsv_to_rgb(h_degree + i * h_offset, 1, 255))
        draw.circle((x,y), radius= radius, fill=hsv_rgb)
        draw.circle((x,y), radius= radius -10, fill=color.rgb)

        
        




    









    image.alpha_composite(ColorBox.SatValBox(color_list, inner_square_size,point_size=10,border=border, border_width=0,fill_with_color=False),(inner_square_offset, inner_square_offset))





    image.show()



if __name__ == "__main__":
    main()

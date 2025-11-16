# from src.ColorBox import *
# from src.ColorWheel import *
# from src.ColorWheelBox import *
from src import ColorBox
from src.Rgb import Rgb
from src.Swatch import SwatchMaker
from src.Utils import *
import src.ColorWheel as ColorWheel
from PIL import Image, ImageDraw, ImageFont
from math import sqrt, asin

import time



def main():
    time.sleep(.5)
    # print("Py Color Swatch Builder")
    # color = Rgb((1,2,3))
    # print(color)
    SwatchMaker(new_medium_swatch)

def new_medium_swatch(color_list: list[Rgb]):
    font = ImageFont.truetype("SourceSans3-Black.ttf", 30)

    size = 700
    width = 1200
    height = 700
    page_size = (width, height)
    ring_size = 600
    hole_size = 500
    border = 50
    midpoint = size//2

    image = Image.new("RGBA", page_size, "white")
    draw = ImageDraw.Draw(image)

    segy = height//(len(color_list)+1)
    for i in reversed(range(len(color_list))):
        color=color_list[i]
        y_start = segy*(i+(0 if i == 0 else 1))
        y_end = segy*(i+2)
        text_y = y_start + segy//2
        text_x = int(ring_size +1.5*border)
        draw.rectangle((0, y_start, 1200, y_end),color.rgb)
        draw.text((text_x, text_y), str(color), "black", font, "lm")
        if i != 0:
            div = color / color_list[0]
            draw.rectangle((900, y_start+10, width-10, y_end-10),div.rgb)
            draw.text((950, text_y), str(div), "black", font, "lm")
    
    div = []
    for i in range(len(color_list)):
        if i != 0:
            div.append(color_list[i]/color_list[0])
        
    div_border = 5
    div_size = min(segy * 2 - 2 * div_border, height//3)
    div_offset = (width - div_border-div_size, div_border)
    div_box = ColorBox.ColorBox(div_size, div[0])
    div_box.paste_into(image, div_offset)
    for d in reversed(div):
        div_box.draw_dot(draw, div_offset, d, 5)
    



    

    
    wheel = ColorWheel.ColorWheel(ring_size + border * 2, ring_size, hole_size,10 )
    dest = (0,0)
    wheel.paste_into(image, dest)

    square_size = int(sqrt(2)*(hole_size/2)) - 8
    square_border = 4
    square_offset = (ring_size - square_size)//2 + border
    square_dest = (dest[0] + square_offset, dest[1] + square_offset)

    square = ColorBox.ColorBox(square_size, color_list[0])
    square.paste_into(image, square_dest)

    for i in reversed(range(len(color_list))):
        color=color_list[i]
        length_offset = i * 20 
        square.draw_dot(draw, square_dest, color, 20+i*3)
        # square.draw_dot(draw, square_dest, color, 2)
        line_bbox = wheel.get_arrow_point(color,dest) + square.get_dot_point(color, square_dest)
        # draw.line(line_bbox, "black", 5)
        # draw.line(line_bbox, color.rgb, 3)
        wheel.draw_arrow(draw, color, dest, from_hole=True, arrow_length=80 + length_offset)
    
    for i in reversed(range(len(color_list))):
        color=color_list[i]
        square.draw_dot(draw, square_dest, color, 5)
        # if i != 0:
        #     square.draw_dot(draw, square_dest, color/color_list[0], 3)
        # wheel.draw_arrow(draw, color, dest, from_hole=True, arrow_length=80 + length_offset)
        # draw.rectangle((800, segy*(i), 1200, segy*(i+1)),color.rgb)
    


        
    
    
        



    image.show()


    image.show()



def medium_swatch(color_list:list[Rgb]):
    size = 800
    page_size = (size + size//2, size)
    ring_size = 400
    border = 100
    hole = 500
    midpoint = size//2
    image = Image.new("RGBA", page_size, "white")
    draw = ImageDraw.Draw(image)
    inner_square_size = int(sqrt(2)*(hole/2)) + 6
    inner_square_offset = (size - inner_square_size) //2
    box_border = 10
    # image.alpha_composite(ColorBox.SatValBox(color_list, inner_square_size,point_size=10,border=10, border_width=4),(inner_square_offset, inner_square_offset))
    image.alpha_composite(ColorBox.SatValBox([color_list[0]], inner_square_size,point_size=10,border=box_border, border_width=4,fill_with_color=True),(inner_square_offset, inner_square_offset))

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

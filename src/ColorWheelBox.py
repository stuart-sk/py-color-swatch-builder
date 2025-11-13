if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0][:-4])

from src.Types import SwatchColor
from PIL import Image, ImageDraw, ImageFont
from colorsys import hsv_to_rgb
from math import cos, sin, radians

def small_rainbow_pi(size, hole, hues:SwatchColor = None, count=360)->Image.Image:
    if not isinstance(hues, list):
        hues = [hues]
    size_offset = 5 
    seg_length = int(360/count)
    # if 360 % seg_length != 0:
    #     seg_length +=1
    img = Image.new('RGBA', size=(size,size), color=(0,0,0,0))
    offset = -150
    start = offset - seg_length//2 -1
    draw = ImageDraw.Draw(img)
    mid_point = size//2
    draw.circle((mid_point,mid_point), mid_point-2, fill="black" )

    for i in range(count): 
        # color
        degree = i * seg_length
        rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,1,255))
        # rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,100,255))
        end = degree + offset + seg_length//2
        # print(locals())
        draw.pieslice([(size_offset,size_offset), (size-size_offset,size-size_offset)], start=start, end=end, fill=rgb)
        start = end 
    
    for hue in reversed(hues):
        line_width = 4
        draw.circle((mid_point, mid_point), hole//2 + 3, fill="black")
        draw.circle((mid_point, mid_point), hole//2, fill=(0,0,0,0))
        degree = hue.hue -150

        x = mid_point+cos(radians(degree)) * mid_point *2//3
        y = mid_point+sin(radians(degree)) * mid_point *2//3
        xm = mid_point+cos(radians(degree)) * mid_point
        ym = mid_point+sin(radians(degree)) * mid_point
        # draw.circle((x,y), radius= line_width//2, fill="black")
        # draw.circle((xm,ym+1), radius= line_width//2+1, fill="black")
        draw.line((x, y, xm, ym+1 ), fill="black", width=line_width+6)
        draw.line((x, y, xm, ym ), fill="white", width=line_width+3)
        draw.line((x, y, xm, ym ), fill=hue.rgb, width=line_width)
    return img


def rainbow_pi(size, count, hue:SwatchColor = None)->Image.Image:
    size_offset = 5 
    seg_length = int(360/count)
    # if 360 % seg_length != 0:
    #     seg_length +=1
    img = Image.new('RGBA', size=(size,size), color=(0,0,0,0))
    offset = -150
    start = offset - seg_length//2 -1
    draw = ImageDraw.Draw(img)
    mid_point = size//2
    draw.circle((mid_point,mid_point), mid_point-2, fill="black" )

    for i in range(count): 
        # color
        degree = i * seg_length
        rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,1,255))
        # rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,100,255))
        end = degree + offset + seg_length//2
        # print(locals())
        draw.pieslice([(size_offset,size_offset), (size-size_offset,size-size_offset)], start=start, end=end, fill=rgb)
        start = end 
    
    if hue:
        line_width = 8
        draw.circle((mid_point, mid_point), size // 3+5, fill="black")
        draw.circle((mid_point, mid_point), size // 3+2, fill=(0,0,0,0))
        # draw.circle((mid_point, mid_point), size // 3+2, fill="black")
        # draw.circle((mid_point, mid_point), size // 3-1, fill=(0,0,0,0))
        # draw.circle((mid_point, mid_point), size // 2-6, fill="black")
        # draw.circle((mid_point, mid_point), size // 2-9, fill=(0,0,0,0))
        degree = hue.hue -150
        x = mid_point+cos(radians(degree)) * mid_point *2//3
        y = mid_point+sin(radians(degree)) * mid_point *2//3
        xm = mid_point+cos(radians(degree)) * mid_point
        ym = mid_point+sin(radians(degree)) * mid_point
        # draw.circle((x,y), radius= line_width//2, fill="black")
        # draw.circle((xm,ym+1), radius= line_width//2+1, fill="black")
        draw.line((x, y+1, xm, ym+1 ), fill="black", width=line_width+6)
        draw.line((x, y, xm, ym ), fill="white", width=line_width)
        # xm = mid_point+cos(radians(degree)) * mid_point*.97
        # ym = mid_point+sin(radians(degree)) * mid_point*.97
        draw.line((x, y, xm, ym ), fill=hue.rgb, width=line_width-2)
        l = int(line_width *1.25)
        print(degree)
        degree_offset = 30
        points = []
        for d in [degree +180 + degree_offset , degree +180 - degree_offset]:
            dx = cos(radians(d)) * l + x
            dy = sin(radians(d)) * l + y

            # draw.line((x, y, dx, dy ), fill="black", width=line_width)
            # draw.circle((dx,dy), radius= line_width//2, fill="black")
            print(d)
            points.append((dx,dy))
        
        distance =int(dist((mid_point,mid_point), points[0]) //1.2)
        # distance = dist((mid_point,mid_point), points[0]) - 6
        print(distance)
        #draw.arc((mid_point-distance, mid_point-distance, mid_point+distance, mid_point+distance),(degree + degree_offset//2) +1, degree-degree_offset//2 -1 , fill="black", width=line_width)
        draw.rectangle((mid_point-distance-1, mid_point-distance-1, mid_point+distance+1, mid_point+distance+1), fill="black", width=3)
        cube = make_color_cube(int(distance*2), hue)
        img.alpha_composite(cube,(int(mid_point-distance), int(mid_point-distance)))

        #draw.rectangle((mid_point-distance, mid_point-distance, mid_point+distance, mid_point+distance), fill=hue.rgb, width=3)
        s_rel = int(mid_point -distance + 2*distance * hue.saturation / 100)
        v_rel = int(mid_point - distance + 2*distance - 2*distance * hue.value / 100)

        text = f"{hue.hue}\n{hue.saturation}\n{hue.value}"
        font = ImageFont.truetype("arialbd.ttf", 20)
        #draw.text((mid_point,size - 3), font=font, text=text, fill="white", anchor="mb",stroke_fill="black", stroke_width=3)
        #draw.multiline_text((mid_point,mid_point), font=font, text=text, fill="white", stroke_fill="black", stroke_width=3, align="center")
        draw.circle((s_rel, v_rel), 4, "black")
        draw.circle((s_rel, v_rel), 2, "white")
    return img

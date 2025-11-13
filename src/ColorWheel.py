if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0][:-4])
    def main():
        #colorwheel(100).show()
        small_rainbow_pi(400,100,SwatchColor((256,0,0))).show()


from src.Types import SwatchColor
from PIL import Image, ImageDraw
from colorsys import hsv_to_rgb
from math import cos, sin, radians




def colorwheel(size, hue:SwatchColor|None = None, use_sat_val = False, count=360):
    image = Image.new("RGBA", (size,size), color=(0,0,0,0))
    draw = ImageDraw.Draw(image)
    seg_length = int(360/count)
    offset = -150
    start = offset - seg_length//2 -1
    for i in range(count): 
        # color
        degree = i * seg_length

        if not hue or not use_sat_val:
            rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,1,255))
        else:
            hsv = hue[0].hsv
            rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,hsv[1],hsv[2]))

        end = degree +offset + seg_length//2
        # print(locals())
        draw.pieslice([(0,0), (size,size)], start=start, end=end, fill=rgb)
        start = end 
    return image


def small_rainbow_pi(size, hole, hues:SwatchColor = None, line_width = 20,count=360, use_sat_val = False)->Image.Image:
    if not isinstance(hues, list):
        hues = [hues]
    
    have_color = len(hues) > 0
    
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
    
    img.alpha_composite(colorwheel(size-2*size_offset,None if not have_color else hues[0]), (size_offset,size_offset))
    

    # for i in range(count): 
    #     # color
    #     degree = i * seg_length

    #     if use_sat_val:

    #         if len(hues) > 0:
    #             hsv = hues[0].hsv
    #             rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,hsv[1],hsv[2]))
    #         else:
    #             rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,1,255))
    #     else:
    #         rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,1,255))
    #     # rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,100,255))
    #     end = degree + offset + seg_length//2
    #     # print(locals())
    #     draw.pieslice([(size_offset,size_offset), (size-size_offset,size-size_offset)], start=start, end=end, fill=rgb)
    #     if use_sat_val:

    #         draw.pieslice([(size_offset,size_offset), (size-size_offset,size-size_offset)], start=start, end=end, fill=rgb)
    #     start = end 
    
    for hue in reversed(hues):
        bar_length = (size-hole)//2
        draw.circle((mid_point, mid_point), hole//2 + 3, fill="black")
        draw.circle((mid_point, mid_point), hole//2, fill=(0,0,0,0))
        degree = hue.hue -150


        # Draw Lines

        #line_colors = ["black", "white", hue.rgb]
        line_colors = ["black", hue.rgb]
        for i in range(len(line_colors)):
            line_offset = 4 * i
            x = mid_point+cos(radians(degree)) * (hole//2 + line_offset)
            y = mid_point+sin(radians(degree)) * (hole//2 +line_offset)
            xm = mid_point+cos(radians(degree)) * (mid_point -line_offset)
            ym = mid_point+sin(radians(degree)) * (mid_point-line_offset)

            draw.line((x, y, xm, ym ), fill=line_colors[i], width=line_width-line_offset)

        # draw.line((x, y, xm, ym+1 ), fill="black", width=line_width)
        # draw.line((x, y, xm, ym ), fill="white", width=line_width - 4)
        # draw.line((x, y, xm, ym ), fill=hue.rgb, width=line_width-8)


        # draw.circle((x,y), radius= line_width//2, fill="black")
        # draw.circle((xm,ym+1), radius= line_width//2+1, fill="black")
    return img
if __name__ == "__main__":
    main()
if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0][:-4])
    def main():
        image = Image.new("RGBA", (500,500),color="white")
        draw = ImageDraw.Draw(image)
        wheel = ColorWheel(400,300,200,10 )
        dest = (40,20)
        wheel.paste_into(image, dest)
        wheel.draw_bar(draw, SwatchColor("red"), dest)
        wheel.draw_arrow(draw, SwatchColor("red"), dest)
        wheel.draw_bar(draw, SwatchColor("oldlace"), dest)
        wheel.draw_arrow(draw, SwatchColor("oldlace"), dest, from_hole=True, arrow_length=80)
        image.show()

        # #colorwheel(100).show()
        # small_rainbow_pi(400,100,SwatchColor((256,0,0))).show()


from dataclasses import dataclass, field
from src.Color import SwatchColor
from PIL import Image, ImageDraw
from colorsys import hsv_to_rgb
from math import cos, sin, radians


@dataclass
class ColorWheel:
    size: int
    wheel_size: int
    inner_hole: int = field(default=0)
    line_width: int = field(default=0)
    use_sat_val: bool = field(default=False)
    border_color: SwatchColor = field(default=SwatchColor("black"))
    coun:int =field(default=360)

    def __post_init__(self):
        self.mid_point = self.size//2

    def paste_into(self, image: Image.Image, dest: tuple):
        # mid_point = self.size//2
        wheel_image = Image.new("RGBA", (self.size, self.size))
        draw = ImageDraw.Draw(wheel_image)
        # Draw border
        if self.line_width > 0:
            # line_start = (self.size - self.wheel_size)//2 - self.line_width
            draw.circle((self.mid_point, self.mid_point), self.wheel_size//2 +self.line_width, fill=self.border_color.rgb)
        # Draw color_wheel

        wheel_offset =  (self.size-self.wheel_size) //2
        wheel_image.alpha_composite(colorwheel(self.wheel_size),(wheel_offset, wheel_offset))
        # Draw hole
        if self.inner_hole > 0:
            if self.line_width > 0:
                draw.circle((self.mid_point, self.mid_point), self.inner_hole//2, fill=self.border_color.rgb)
            draw.circle((self.mid_point, self.mid_point), self.inner_hole//2 - self.line_width, fill=(0,0,0,0))
        image.alpha_composite(wheel_image, dest)
    def draw_bar(self, draw: ImageDraw.ImageDraw, colors: SwatchColor, dest:tuple,  bar_width = 15, bar_fill = SwatchColor()):
        colors = [colors] if isinstance(colors, SwatchColor) else colors

        for hue in reversed(colors):
            bar_length = (self.size-self.inner_hole)//2
            degree = hue.hue -150
            line_colors = ["black", hue.rgb]
            for i in range(len(line_colors)):
                line_offset = 4 * i
                x =  dest[0] + self.mid_point+cos(radians(degree)) * (self.inner_hole//2)# -line_offset)
                y =  dest[1] + self.mid_point+sin(radians(degree)) * (self.inner_hole//2)# -line_offset)
                xm = dest[0] + self.mid_point+cos(radians(degree)) * (self.wheel_size//2)# +line_offset)
                ym = dest[1] + self.mid_point+sin(radians(degree)) * (self.wheel_size//2)# +line_offset)
                draw.line((x, y, xm, ym ), fill=line_colors[i], width=bar_width-line_offset)
    def draw_arrow(self, draw: ImageDraw.ImageDraw, colors: SwatchColor, dest:tuple,  arrow_length = 30, arrow_degrees = 30, from_hole = False, bar_fill = SwatchColor()):
        colors = [colors] if isinstance(colors, SwatchColor) else colors
        for hue in reversed(colors):
            bar_length = (self.size-self.inner_hole)//2
            degree = hue.hue -150
            arrow_dir = degree
            # arrow_dir += 180

            line_colors = ["black", hue.rgb]
            for i in range(len(line_colors)):
                color = line_colors[i]
                line_offset = 8 * i
                radius = ((self.inner_hole//2)-self.line_width if from_hole else (self.wheel_size//2 + self.line_width)) + line_offset
                # line_colors = ["black", hue.rgb]
                x = dest[0] + self.mid_point+cos(radians(degree)) * radius
                y = dest[1] + self.mid_point+sin(radians(degree)) * radius

                offset_length = arrow_length - line_offset

                print(f"drawing color {color}")
                for t in ["i", "color", "line_offset", "radius", "x", "y", "offset_length"]:
                    print(f"- {t}: {locals()[t]}")
                
                pi_radius = arrow_length-1.5*line_offset

                bbox = (x -pi_radius, y -pi_radius, x + pi_radius, y + pi_radius)
                draw.pieslice(bbox, arrow_dir - (arrow_degrees - 6*i)//2, arrow_dir + (arrow_degrees -6*i)//2, color)

    def get_arrow_point(self, color:SwatchColor, dest: tuple = (0,0))->tuple:
        degree = color.hue -150
        arrow_dir = degree
        radius = self.inner_hole//2
        # line_colors = ["black", hue.rgb]
        x = dest[0] + self.mid_point+cos(radians(degree)) * radius
        y = dest[1] + self.mid_point+sin(radians(degree)) * radius
        return (x,y)





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
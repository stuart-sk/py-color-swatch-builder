#import PIL
if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0].split("src")[0])
from pynput import keyboard
from pynput import mouse
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from colorsys import rgb_to_hsv, hsv_to_rgb
from math import sin, cos, radians
from src.Swatch import SwatchMaker
from src.Types import SwatchColor
from src.ColorBox import SatValBox
from src.ColorWheel import small_rainbow_pi
# from modules.swatch_classes import SwatchColor, SwatchWheel, rainbow_pi, small_rainbow_pi
import numpy as np
import math

def main():
    print("Hello from py-color-swatch-builder!")
    #large = LargeSwatches()
    small = SmallSwatches()
    #rainbow_pi(200,360, SwatchColor((67, 196, 193))).show()
        # draw.line((mid_point, mid_point, mid_point+x, mid_point+y), fill="black")




def SimpleSwatch(color_list:list[SwatchColor]):
    color_list
    unit = 280
    base = 200
    base_offset = (unit - base)//2
    border = 100
    count = len(color_list)
    width = border  *2 +   count*unit
    height = border * 2 + 2 * unit
    image = Image.new("RGBA",(width,height), color="white")
    ellipse_side_radius = base//1.45 
    font = ImageFont.truetype("SourceSans3-Black.ttf", 30)
    font_offset = 22
    texty_offset = 35

    draw = ImageDraw.Draw(image)
    small_ring_size = border + base_offset - 10
    small_ring_offset = (base - small_ring_size)//2

    for index in range(len(color_list)):
        swatch = color_list[index]
        offsetx = border + index * unit  + base_offset
        offsety = border + base_offset
        textx_offset = offsetx + base//2

        draw.rectangle((offsetx, offsety, offsetx + base, height-offsety), fill=swatch.rgb)
        draw.ellipse((offsetx, offsety - ellipse_side_radius, offsetx + base, offsety + ellipse_side_radius), fill= swatch.rgb)
        draw.ellipse((offsetx, height - offsety - ellipse_side_radius, offsetx + base, height - offsety + ellipse_side_radius), fill= swatch.rgb)



        draw.text((textx_offset, texty_offset), font=font, text=str(swatch.hue), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
        draw.text((textx_offset, texty_offset+font_offset), font=font, text=str(swatch.saturation), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
        draw.text((textx_offset, texty_offset+2*font_offset), font=font, text=str(swatch.value), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)

        if index == 0:
            image.alpha_composite(SatValBox(color_list,base+10, point_size=8, border=10), (offsetx -5,offsety-5))
            image.alpha_composite(small_rainbow_pi(small_ring_size, 80, color_list),(offsetx+small_ring_offset, 5))
        else:
            image.alpha_composite(small_rainbow_pi(small_ring_size, 80, swatch),(offsetx+small_ring_offset, 5))
            image.alpha_composite(SatValBox(swatch,base+10, point_size=8, border=10, fill_with_color=False), (offsetx -5,offsety-5))


        offsety = border + unit + base_offset

        if(index != 0):
            div = swatch/color_list[0]
            draw.rectangle((offsetx, offsety, offsetx + base, offsety+base), fill=div.rgb)

            
            image.alpha_composite(small_rainbow_pi(small_ring_size, 80, div,),(offsetx+small_ring_offset, height-small_ring_size-5))
            draw.text((textx_offset, texty_offset + offsety + base), font=font, text=str(div.hue), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
            draw.text((textx_offset, texty_offset + offsety+base +font_offset), font=font, text=str(div.saturation), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
            draw.text((textx_offset, texty_offset + offsety+base +2*font_offset), font=font, text=str(div.value), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
            # image.alpha_composite(SatValBox(div,base+10, point_size=3, border=5), (offsetx -5,offsety-5))
            image.alpha_composite(SatValBox(div,base+10, point_size=8, border=10,fill_with_color=False), (offsetx -5,offsety-5))


        else:
            offsetx = border + base_offset
            offset_adjustment = 50
            draw.rectangle((offsetx-offset_adjustment, offsety, width-border-base_offset+offset_adjustment, offsety + base), fill=swatch.rgb)
            # draw.ellipse((offsetx- ellipse_side_radius-offset_adjustment, offsety , offsetx + ellipse_side_radius-offset_adjustment, offsety+base), fill= swatch.rgb)
            # draw.ellipse((width-border-base_offset -ellipse_side_radius+offset_adjustment, offsety, width-border-base_offset +ellipse_side_radius+offset_adjustment,offsety + base), fill= swatch.rgb)
            div_list = list(x/color_list[0] for x in color_list)

            image.alpha_composite(SatValBox(div_list,base+10, point_size=8, border=10), (offsetx -5,offsety-5))
            
    # image.alpha_composite(rainbow_pi(unit+base_offset,360,list[0]), (base_offset, height-border -unit-base_offset))


    image.show()

class SmallSwatches:
    def __init__(self):
        self.color_list:list[SwatchColor] = []
        #ColorPicker(self.add_color, self.make_swatch_v3)
        SwatchMaker(lambda e: SimpleSwatch(e))
    
    # def on_trigger(f):
    #     SimpleSwatch(self.color_list)

    def add_color(self, rgb):
        self.color_list.append(SwatchColor(rgb))
        # print(SwatchColor(rgb).hsv)
        # self.make_color_cube(200, SwatchColor(rgb)).show()

    # use a vertical setup. Move Colors to far left and right.
    def make_swatch_v3(self):
        count = len(self.color_list)
        base = self.color_list[0]
        bar_width = 53 
        size_unit = 120
        half_unit = 60
        border_unit = 60
        bar_offset = (size_unit - bar_width) // 2

        img = Image.new("RGBA",(size_unit*2 + 2*border_unit, size_unit *(count) + 2 * border_unit), color = "white" )
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("SourceSans3-Black.ttf", 20)
        for index in range(len(self.color_list)):
            swatch = self.color_list[index]
            offsetx = size_unit * index + border_unit
            offsetx = size_unit * index + border_unit
            textx_offset = offsetx + half_unit
            texty_upper = border_unit -4
            texty_lower = border_unit + 2*size_unit + 4


            if index == 0:
                draw.rounded_rectangle((5,size_unit+border_unit+bar_offset, size_unit*count + border_unit, size_unit+border_unit+bar_offset+bar_width), radius=bar_width//4, fill=swatch.rgb)
                img.alpha_composite(rainbow_pi(size_unit,360, swatch),(offsetx, size_unit + border_unit))
            else:
                div = swatch/self.color_list[0]
                draw.rounded_rectangle(( offsetx+bar_offset,5, offsetx+ bar_offset+bar_width,2*size_unit + 2 * border_unit -5), radius=bar_width//4, fill=div.rgb)

                img.alpha_composite(rainbow_pi(size_unit,360, swatch),(offsetx, size_unit + border_unit))
                img.alpha_composite(rainbow_pi(size_unit,360, div),(offsetx, border_unit))
                draw.text((textx_offset, 7), font=font, text=str(div.hue), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
                draw.text((textx_offset, 24), font=font, text=str(div.saturation), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
                draw.text((textx_offset, 41), font=font, text=str(div.value), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
                # draw.text((offsetx, 5), font=font, text=str(div.hue), fill="black", anchor="la",stroke_fill=div.rgb, stroke_width=2)
                # draw.multiline_text((textx_offset, texty_upper), font=font, text=f"{div.hue}\n{div.saturation}\n{div.value}", fill="black",align="left",stroke_fill=div.rgb, stroke_width=2, spacing=0)

            #text lower
            draw.text((textx_offset, texty_lower), font=font, text=str(swatch), fill="black", anchor="mt",stroke_fill=swatch.rgb, stroke_width=2)

        img.show()





        print("Hello From Small Swatches")
    
    def make_swatch(self):
        count = len(self.color_list)
        base = self.color_list[0]
        bar_width = 53 
        size_unit = 200
        half_unit = 60
        border_unit = 60
        bar_offset = (size_unit - bar_width) // 2

        img = Image.new("RGBA",(size_unit *(count) + 2 * border_unit, size_unit*2 + 2*border_unit), color = "white" )
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("SourceSans3-Black.ttf", 20)
        for index in range(len(self.color_list)):
            swatch = self.color_list[index]
            offsetx = size_unit * index + border_unit
            textx_offset = offsetx + half_unit
            texty_upper = border_unit -4
            texty_lower = border_unit + 2*size_unit + 4



            if index == 0:
                draw.rounded_rectangle((5,size_unit+border_unit+bar_offset, size_unit*count + border_unit, size_unit+border_unit+bar_offset+bar_width), radius=bar_width//4, fill=swatch.rgb)
                img.alpha_composite(rainbow_pi(size_unit,360, swatch),(offsetx, size_unit + border_unit))
            else:
                div = swatch/self.color_list[0]
                draw.rounded_rectangle(( offsetx+bar_offset,5, offsetx+ bar_offset+bar_width,2*size_unit + 2 * border_unit -5), radius=bar_width//4, fill=div.rgb)

                img.alpha_composite(rainbow_pi(size_unit,360, swatch),(offsetx, size_unit + border_unit))
                img.alpha_composite(rainbow_pi(size_unit,360, div),(offsetx, border_unit))
                draw.text((textx_offset, 7), font=font, text=str(div.hue), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
                draw.text((textx_offset, 24), font=font, text=str(div.saturation), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
                draw.text((textx_offset, 41), font=font, text=str(div.value), fill="black", anchor="mt",stroke_fill="white", stroke_width=2)
                # draw.text((offsetx, 5), font=font, text=str(div.hue), fill="black", anchor="la",stroke_fill=div.rgb, stroke_width=2)
                # draw.multiline_text((textx_offset, texty_upper), font=font, text=f"{div.hue}\n{div.saturation}\n{div.value}", fill="black",align="left",stroke_fill=div.rgb, stroke_width=2, spacing=0)

            #text lower
            draw.text((textx_offset, texty_lower), font=font, text=str(swatch), fill="black", anchor="mt",stroke_fill=swatch.rgb, stroke_width=2)

        img.show()





        print("Hello From Small Swatches")



class LargeSwatches:
    def __init__(self):
        self.color_list:list[SwatchColor] = []
        SwatchMaker(self.add_color, self.make_swatch)
    
    def add_color(self, rgb):
        self.color_list.append(SwatchColor(rgb))



    def color_square(self, size, rgb, dot_size) -> Image.Image:
            border_size = size
            size = size - 2 * dot_size
            h,s,v = rgb_to_hsv(*rgb)
            hue = int(h*360)
            saturation = int(s*100)
            value = int(v /255 * 100)


            s_rel = dot_size + int(size * s)
            v_rel = dot_size + int(size - size * v / 255)
            print(f'srel: {s_rel}, v_rel: {v_rel}, s:{s}, v:{v}')
                
            norm_img =Image.new('RGB', (size, size), rgb)
            border_img = Image.new('RGB', (border_size, border_size), "white")
            border_img.paste(norm_img, (dot_size, dot_size))

            draw = ImageDraw.Draw(border_img)
                
            text = f"{hue}  {saturation}  {value}"
            font = ImageFont.truetype("arialbd.ttf", 20)
            font_width = font.getlength(text)
                
            fonty = v_rel
            if fonty + dot_size > border_size/ 2:
                fonty -= 3 * dot_size
            else:
                fonty += 2*dot_size
                
            if (s_rel + dot_size - font_width / 2) < dot_size:
                fontx = int(font_width/2 + 2*dot_size)
            elif s_rel + 2 * dot_size + font_width / 2 > border_size:
                fontx = 2 * dot_size + font_width / 2
            else:
                fontx = dot_size + s_rel



            if fonty + dot_size > border_size/ 2:
                fonty -= 3 * dot_size
            else:
                fonty += 2*dot_size


            #draw.text(xy=(dot_size + size/2, dot_size + size - 10), text=f"{hue}  {saturation}  {value}", anchor="mb", font=font, stroke_fill="black", stroke_width=2)
            draw.text(xy=(fontx,fonty), text=f"{hue}  {saturation}  {value}", anchor="mt", font=font, stroke_fill="black", stroke_width=2)
            draw.circle((s_rel,v_rel), dot_size, fill="black")
            draw.circle((s_rel,v_rel), dot_size-3, fill="white")

            return border_img
        

    def make_swatch(self):
        size = 300
        dot_size = 10
        width = (len(self.color_list) + 1) *(size)
        height = 2 * size
        img = Image.new('RGBA', (width,height), self.color_list[0].rgb)
        base =self.color_list[0].rgb
        rgb_wheel = SwatchWheel("wheel.png", size, dot_size)
        drgb_wheel = SwatchWheel("wheel.png", size, dot_size)

        for i in range(1,len(self.color_list)):
            rgb = self.color_list[i].rgb
            drgb = tuple((x*255)//y for x, y in zip(rgb, base))

            #normal
            img.paste(self.color_square(size, rgb, dot_size), (size*i, 0) )
            rgb_wheel.add_point(rgb)

            #divided
            img.paste(self.color_square(size, drgb, dot_size), (size*i, size) )
            drgb_wheel.add_point(rgb)

            # print(f"{i} ---- \n - rgb: {rgb}\n - drgb: {drgb}\n - base: {base}")

            draw = ImageDraw.Draw(img)
                        
            h,s,v = rgb_to_hsv(*rgb)
            s_rel = int(size * s)
            v_rel = int(size - size * v / 255)
            draw.circle((s_rel, v_rel), dot_size+2, "black")
            draw.circle((s_rel, v_rel), dot_size, rgb)
                    
            h,s,v = rgb_to_hsv(*drgb)
            s_rel = int(size * s)
            v_rel = int(size - size * v / 255) + size
            draw.circle((s_rel, v_rel), dot_size+2, "black")
            draw.circle((s_rel, v_rel), dot_size, drgb)
            
        wheel_x_offset = len(self.color_list) * size
        img.alpha_composite(rgb_wheel.wheel(), (wheel_x_offset, 0))
        img.alpha_composite(drgb_wheel.wheel(), (wheel_x_offset, size))
        img.show()
            
if __name__ == "__main__":
    main()
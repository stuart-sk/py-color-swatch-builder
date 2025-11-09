#import PIL
from pynput import keyboard
from pynput import mouse
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from colorsys import rgb_to_hsv, hsv_to_rgb
from math import sin, cos, radians
from modules.color_picker import ColorPicker
from modules.swatch_classes import SwatchColor, SwatchWheel, rainbow_pi
import math

def main():
    print("Hello from py-color-swatch-builder!")
    #large = LargeSwatches()
    small = SmallSwatches()
    #rainbow_pi(200,360, SwatchColor((67, 196, 193))).show()
        # draw.line((mid_point, mid_point, mid_point+x, mid_point+y), fill="black")





class SmallSwatches:
    def __init__(self):
        self.color_list:list[SwatchColor] = []
        ColorPicker(self.add_color, self.make_swatch)
    
    def add_color(self, rgb):
        self.color_list.append(SwatchColor(rgb))
    
    def make_swatch(self):
        count = len(self.color_list)
        base = self.color_list[0]
        bar_width = 53 
        size_unit = 120
        half_unit = 60
        border_unit = 30
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
                draw.text((textx_offset, texty_upper), font=font, text=str(div), fill="black", anchor="mb",stroke_fill=div.rgb, stroke_width=2)

            #text lower
            draw.text((textx_offset, texty_lower), font=font, text=str(swatch), fill="black", anchor="mt",stroke_fill=swatch.rgb, stroke_width=2)

        img.show()





        print("Hello From Small Swatches")



class LargeSwatches:
    def __init__(self):
        self.color_list:list[SwatchColor] = []
        ColorPicker(self.add_color, self.make_swatch)
    
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
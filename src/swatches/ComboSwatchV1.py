if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0].split("src")[0])

#import PIL
from pynput import keyboard
from pynput import mouse
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from colorsys import rgb_to_hsv, hsv_to_rgb
from math import sin, cos, radians

# def main():
#     print("Hello from py-color-swatch-builder!")

class SwatchColor:
    def __init__(self, rgb):
        self.rgb = rgb 
        self.hsv = rgb_to_hsv(*rgb)
        self.hue = int(self.hsv[0]*360)
        self.hue_rgb = tuple(int(x) for x in hsv_to_rgb(self.hsv[0], 1, 256))
        self.saturation = int(self.hsv[1]*100)
        self.value = int(self.hsv[2] /255 * 100)

class Swatch_Builder:


    class SwatchWheel:
        def __init__(self, file, size, dot_size):
            self._wheel = Image.open(file, ).resize((size, size)).convert("RGBA")
            self.size = size
            self.color_list:list[SwatchColor] = []
            self.dot_size = dot_size
            self.center = self.size / 2
            self.radius = .45*self.size
            self.sat_strength = .8 #percent of the radius distance of points influenced by saturation.


        # build new wheel whenever called. This allows for deleting points.
        def wheel(self):

            copy = self._wheel.copy()
            draw = ImageDraw.Draw(copy)

            max_sat = max(self.color_list, key=lambda color: color.saturation).saturation
            min_sat = min(self.color_list, key=lambda color: color.saturation).saturation

            for i in reversed(range(len(self.color_list))):
                color = self.color_list[i]
                if False:
                    rel_saturation = (color.saturation - min_sat) / (max_sat-min_sat)
                    sat_dist = int(self.radius * (1-self.sat_strength) 
                                + rel_saturation * self.radius * self.sat_strength)
                
                rel_dist = (len(self.color_list) -1 -i) / (len(self.color_list))
                dist = int(self.radius * (1-self.sat_strength) 
                            + rel_dist * self.radius * self.sat_strength)
                


                # Hue in degrees / 360.
                # Note that CSP wheel is counterclockwise.
                # Also note that the top of the circle is 60 instead of 90.
                # with unit circle, or hyp = 1
                # sin(theta) = opp / hyp = opp  = Y
                # cos(theta) = adjacent / hyp = adjacent = X
                degrees = color.hue - 150





                xy = (int(self.center + cos(radians(degrees)) * dist),
                      int(self.center + sin(radians(degrees)) * dist))

                xyl = (int(self.center + cos(radians(degrees)) * self.radius),
                       int(self.center + sin(radians(degrees)) * self.radius))


                #print(f"hue: {hue} degrees: {degrees}, x: {x}, y:{y}, cos:{cos(degrees)}, sin:{sin(degrees)}")

                # draw.line([xy, xyl], fill="white", width=5)
                draw.line([xy, xyl], fill=color.hue_rgb, width=3)
                draw.circle(xy, self.dot_size + 2, "black")
                draw.circle(xy, self.dot_size, color.rgb)

            return copy
        
        def add_point(self, rgb):
            self.color_list.append(SwatchColor(rgb))

    def __init__(self):
        self.color_list = []

    def start(self):
        with keyboard.Listener(on_release = self.onRel) as klstnr:
            with mouse.Listener(on_click = self.onClick) as mlstnr:
                klstnr.join()
                mlstnr.join()
                self.mlstnr = mlstnr

    def getHex(self, rgb):
        return '%02X%02X%02X'%rgb

    def checkColor(self, x,y):
        bbox = (x,y,x+1,y+1)
        #im = ImageGrab.grab(bbox=bbox)
        im = ImageGrab.grab(all_screens=True, bbox=bbox)
        rgbim = im.convert('RGB')
        r,g,b = rgbim.getpixel((0,0))
        print(f'COLOR: rgb{(r,g,b)} | HEX #{self.getHex((r,g,b))} | x:{x} y:{y}')
        self.color_list.append((r,g,b))
        
    
    def onClick(self, x,y, button, pressed):
        if pressed and button == mouse.Button.left:
            self.checkColor(x,y)
    
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
        img = Image.new('RGBA', (width,height), self.color_list[0])
        base =self.color_list[0]
        rgb_wheel = self.SwatchWheel("wheel.png", size, dot_size)
        drgb_wheel = self.SwatchWheel("wheel.png", size, dot_size)

        for i in range(1,len(self.color_list)):
            rgb = self.color_list[i]
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

    def onRel(self, key):
        if key == keyboard.Key.esc:

            self.make_swatch()
        
            





            self.mlstnr.stop()
            return False








if __name__ == "__main__":
    swatch_builder = Swatch_Builder()
    swatch_builder.start()







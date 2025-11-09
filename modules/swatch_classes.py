from pynput import keyboard
from pynput import mouse
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from colorsys import rgb_to_hsv, hsv_to_rgb
from math import sin, cos, radians, dist


def main():
    # a = SwatchColor((100, 100, 100))
    # b = SwatchColor((50, 50, 50))
    a = SwatchColor((255, 226, 206))
    b = SwatchColor((192, 185, 207))
    print((a*b).rgb)
    print((b*a).rgb)
    print((a/b).rgb)
    print((b/a).rgb)


class SwatchColor:
    def __init__(self, rgb):
        self.rgb = rgb 
        self.hsv = rgb_to_hsv(*rgb)
        self.hue = int(self.hsv[0]*360)
        self.hue_rgb = tuple(int(x) for x in hsv_to_rgb(self.hsv[0], 1, 256))
        self.saturation = int(self.hsv[1]*100)
        self.value = int(self.hsv[2] /255 * 100)
    
    def __mul__(self, r):
        return SwatchColor(tuple(int(max(0,min(255,(x/255)*y))) for x, y in zip(self.rgb, r.rgb)))

    def __truediv__(self, r):
        return SwatchColor(tuple(x if y == 0 else int(max(0,min(255,(x*255)//y))) for x, y in zip(self.rgb, r.rgb)))
    
    def __str__(self):
        return f"{self.hue},{self.saturation},{self.value}"


def rainbow_pi(size, count, hue:SwatchColor = None)->Image.Image:
    size_offset = 4 
    seg_length = int(360/count)
    # if 360 % seg_length != 0:
    #     seg_length +=1
    img = Image.new('RGBA', size=(size,size), color=(0,0,0,0))
    offset = -150
    start = offset - seg_length//2 -1
    draw = ImageDraw.Draw(img)
    mid_point = size//2
    draw.circle((mid_point,mid_point), mid_point, fill="black" )

    for i in range(count): 
        # color
        degree = i * seg_length
        rgb = tuple(int(x) for x in hsv_to_rgb(degree/360.0,hue.saturation/100,hue.value*2.55))
        end = degree + offset + seg_length//2
        # print(locals())
        draw.pieslice([(size_offset,size_offset), (size-size_offset,size-size_offset)], start=start, end=end, fill=rgb)
        start = end 
    
    if hue:
        line_width = 8
        draw.circle((mid_point, mid_point), size // 3+2, fill="black")
        draw.circle((mid_point, mid_point), size // 3-1, fill=(0,0,0,0))
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
        
        #distance = math.dist((mid_point,mid_point), points[0]) + line_width //2
        distance = dist((mid_point,mid_point), points[0]) - 6
        print(distance)
        #draw.arc((mid_point-distance, mid_point-distance, mid_point+distance, mid_point+distance),(degree + degree_offset//2) +1, degree-degree_offset//2 -1 , fill="black", width=line_width)
        draw.rectangle((mid_point-distance-1, mid_point-distance-1, mid_point+distance+1, mid_point+distance+1), fill="black", width=3)
        draw.rectangle((mid_point-distance, mid_point-distance, mid_point+distance, mid_point+distance), fill=hue.rgb, width=3)
        s_rel = int((size-distance)/2 + distance * hue.saturation / 100)
        v_rel = int((size-distance)/2 + distance - distance * hue.value / 100)

        text = f"{hue.hue}\n{hue.saturation}\n{hue.value}"
        font = ImageFont.truetype("arialbd.ttf", 20)
        #draw.text((mid_point,size - 3), font=font, text=text, fill="white", anchor="mb",stroke_fill="black", stroke_width=3)
        #draw.multiline_text((mid_point,mid_point), font=font, text=text, fill="white", stroke_fill="black", stroke_width=3, align="center")
        draw.circle((s_rel, v_rel), 4, "black")
        draw.circle((s_rel, v_rel), 2, "white")
    return img



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
            rel_dist = (len(self.color_list) -1 -i) / (len(self.color_list))
            dist = int(self.radius * (1-self.sat_strength) 
                        + rel_dist * self.radius * self.sat_strength)

            degrees = color.hue - 150

            xy = (int(self.center + cos(radians(degrees)) * dist),
                    int(self.center + sin(radians(degrees)) * dist))

            xyl = (int(self.center + cos(radians(degrees)) * self.radius),
                    int(self.center + sin(radians(degrees)) * self.radius))

            # draw.line([xy, xyl], fill="white", width=5)
            draw.line([xy, xyl], fill=color.hue_rgb, width=3)
            draw.circle(xy, self.dot_size + 2, "black")
            draw.circle(xy, self.dot_size, color.rgb)

        return copy
        
    def add_point(self, rgb):
        self.color_list.append(SwatchColor(rgb))

if __name__ == "__main__":
    main()
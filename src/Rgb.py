import collections.abc
from colorsys import rgb_to_hsv, hsv_to_rgb
from math import sqrt
from PIL import ImageColor

def main():
    print(Rgb(0,0,0))
    print(Rgb("white"))
    print(Rgb())
    print(Rgb((0,0,0)))


class Rgb(collections.abc.Sequence):
    def __init__(self, *rgba: tuple):

        if len(rgba) == 0:
            self.rgb = (0,0,0)
        elif isinstance(rgba, str):
            self.rgb = tuple(int(x) for x in ImageColor.getrgb(rgba))
        elif len(rgba) == 1:
            if isinstance(rgba[0], str):
                self.rgb = tuple(int(x) for x in ImageColor.getrgb(rgba[0]))
            else:
                self.rgb = tuple(int(x) for x in rgba[0][:3])
        else:
            self.rgb = tuple(int(x) for x in rgba[:3])
        self.hsv = rgb_to_hsv(self.rgb[0], self.rgb[1], self.rgb[2])
        self.hue = int(self.hsv[0]*360)
        self.hue_rgb = tuple(int(x) for x in hsv_to_rgb(self.hsv[0], 1, 256))
        self.saturation = int(self.hsv[1]*100)
        self.value = int(self.hsv[2] /255 * 100)
    def __len__(self): return len(self.rgb)
    def __getitem__(self, index): return self.rgb[index]
    def __str__(self): return str(self.rgb)
    def __add__(self, r):
        return Rgb(add(self, r))
    def __sub__(self, r):
        return Rgb(sub(self, r))
    def __mul__(self, r):
        return Rgb(mul(self, r))
    def __truediv__(self, r):
        return Rgb(div(self,r))
    def invert(self, rgb = None):
        return Rgb(inv(rgb if rgb else self.rgb))
    def screen(self, r):
        return Rgb(screen(self, r))
    def color_dodge(self, r):
        return Rgb(color_dodge(self, r))
    def linear_dodge(self, r):
        return Rgb(linear_dodge(self, r))
    def hard_light(self, r):
        return Rgb(hard_light(self, r))
    def overlay(self, r):
        return Rgb(hard_light(self, r))
    def soft_light(self, r):
        return Rgb(soft_light(self, r))
    def inv_soft_light(self, r):
        return Rgb(inv_soft_light(self, r))


def inv(l):
    return tuple(255-x for x in l)

def add(l, r):
    return tuple(min(255, x+y) for x,y in zip(l,r))

def sub(l, r):
    return tuple(max(0, x-y) for x,y in zip(l,r))

def avg(l, r):
    return tuple(min(255, (x+y)//2) for x,y in zip(l,r))

def mul(l, r):
    return tuple(min(255, (x/255)*y) for x,y in zip(l,r))

def div(l, r):
    return tuple(x if y == 0 else 
        int(max(0,min(255,(x*255)//y))) for x, y in zip(l, r))
    
def screen(l,r):
    return inv(mul(inv(l), inv(r))) 

def color_dodge(l,r):
    return div(l, inv(r))

def linear_dodge(l,r):
    return add(l,r)

def overlay(l,r):
    return tuple( 
        min(255, 2 * (x/255) * y)
        # 2xy 
        if x < 128 else
        # 1 - 2*(1-x)(1-y) 
        max(0,min(255,255-2*((255-x) / 255 * (255-y)
        ))) for x,y in zip(l,r))
    
def hard_light(l,r):
    return tuple( 
        min(255, 2 * (x/255) * y)
        # 2xy 
        if y < 128 else
        # 1 - 2*(1-x)(1-y) 
        max(0,min(255,255-2*((255-x) / 255 * (255-y)
        ))) for x,y in zip(l,r))

def soft_light(l,r):
    norml = tuple(x / 255 for x in l)
    normr = tuple(y / 255 for y in r)

    # soft_light_norm = tuple(
    #     # 2ab + a**2(1-2b)
    #     2 * x * y + x**2 * (1-2*y)
    #     if y < .5 else 
    #     2 * x *(1-y) + sqrt(x) * (2 * y - 1)
    #     for x,y in zip(norml, normr)
    # )

    soft_light_norm = tuple(
        (1 - 2 * y) * x * x + 2 * y * x
        for x,y in zip(norml, normr)
    )
    return tuple( max(0, min(255,int(255 * x))) for x in soft_light_norm)

def inv_soft_light(l, r):
    norml = tuple(x / 255 for x in l)
    normr = tuple(y / 255 for y in r)

    inv_soft_light_norm = tuple(
        (c - a**2) / (-2 * a**2 + 2*a)
        for a, c in zip(norml, normr)
    )
    return tuple( max(0, min(255,int(255 * x))) for x in inv_soft_light_norm)

if __name__ == "__main__":
    main()
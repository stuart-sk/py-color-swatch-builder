if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0].split("src")[0])

import logging
from pynput import keyboard, mouse
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from collections.abc import Callable

from src.Types import SwatchColor

class SwatchMaker: 

    def __init__(self, on_esc: Callable[[list],None]):
        self.on_esc = on_esc
        self.color_list = []
        with keyboard.Listener(on_release = self.onRel) as klstnr:
            with mouse.Listener(on_click = self.onClick) as mlstnr:
                self.mlstnr = mlstnr
                klstnr.join()
                mlstnr.join()

    def pick_rgb(self, rgb):
        self.color_list.append(SwatchColor(rgb))

    def getHex(self, rgb):
        return '%02X%02X%02X'%rgb

    def checkColor(self, x,y):
        bbox = (x,y,x+1,y+1)
        #im = ImageGrab.grab(bbox=bbox)
        im = ImageGrab.grab(all_screens=True, bbox=bbox)
        rgbim = im.convert('RGB')
        r,g,b = rgbim.getpixel((0,0))
        print(f'COLOR: rgb{(r,g,b)} | HEX #{self.getHex((r,g,b))} | x:{x} y:{y}')
        self.pick_rgb((r,g,b))
        
    
    def onClick(self, x,y, button, pressed):
        if pressed and button == mouse.Button.left:
            self.checkColor(x,y)
    
    def onRel(self, key):
        logger = logging.Logger('catch_all')
        if key == keyboard.Key.esc:
            try:
                self.on_esc(self.color_list)
            except Exception as e:
                logger.error(e, exc_info=True)

                #print(f"ERROR: an error occured in on_esc \n{e}\n{e.with_traceback}")
            finally:
                self.mlstnr.stop()
                return False

if __name__ == "__main__":
    swatch_maker = SwatchMaker(lambda e: (print(x) for x in e))

    # color_picker = ColorPicker(lambda e: print(e), lambda: print("ESCAPE"))

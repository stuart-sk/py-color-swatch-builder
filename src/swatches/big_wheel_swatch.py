from PIL import Image, ImageDraw

if __name__ == "__main__":
    import sys
    sys.path.insert(1, sys.path[0].split("src")[0])
    def main():
        swatch = BigWheelSwatch()


from src.Swatch import SwatchMaker
from src.Types import SwatchColor

class BigWheelSwatch(SwatchMaker):
    def __init__(self):
        self.color_list = []

        super().__init__(self.pick_rgb, self.on_esc)


    def on_esc(self):
        page_size = (600, 600)
        ring_size = 400
        border = 50
        image = Image.new("RGBA", page_size, "white")
        draw = ImageDraw.Draw(image)





        


        
        image.show()




if __name__ == "__main__":
    main()
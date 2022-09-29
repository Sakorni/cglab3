import numpy as np
import tkinter
from PIL import Image, ImageColor


def color_from_rgb(color):
    """
    _color_from_rgb convert color from RGB format into friendly to tkinter color
    """
    color = (color[0], color[1], color[2])
    return "#%02x%02x%02x" % color


def color_from_hex(color):
    return ImageColor.getrgb(color)


class ColorAnalyzer:
    def __init__(self, canvas, default_color):
        self.default_color = default_color
        self.canvas = canvas
        # self.set_analyzed_color(analyzed_color)

    def set_analyzed_color(self, color):
        self.color = color

    def get_color(self, x, y):
        arr = self.canvas.find_overlapping(x, y, x, y)
        if (len(arr) == 0):
            hex_c = self.default_color
        else:
            hex_c = self.canvas.itemcget(arr[-1], "fill")
        rgb = color_from_hex(hex_c)
        return [rgb, hex_c]

    def isEmptyPixel(self, x, y, tolerance=None):
        if (x < 0 or x > self.canvas.winfo_reqwidth()):
            return False
        if (y < 0 or y > self.canvas.winfo_reqheight()):
            return False
        color = self.get_color(x, y)

        if tolerance is None:
            print(f"[{color[1]}], [{self.color[1]}], ({x},{y})")
            return color[1] == self.color[1]

        for i in range(3):
            if abs(color[0][i] - self.color[0][i]) > tolerance[i]:
                return False
        return True


class Drawer:
    def __init__(self, canvas: tkinter.Canvas, color: tuple):
        self.color = color
        self.canvas = canvas

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, tag: str = None):
        """
        drawLine draws a line from x1y1 point to x2y2 point
        """
        tags = ['drawn']
        if not tag is None:
            tags.append(tag)
        self.canvas.create_line(x1, y1, x2, y2,
                                fill=self.color[1], capstyle=tkinter.ROUND,
                                smooth=tkinter.TRUE, splinesteps=36, tags=tags)

    def set_pixel(self, x: int, y: int, b: float = 1.0, tag: str = None):
        tags = ['drawn']
        if not tag is None:
            tags.append(tag)
        new_color = [round(self.color[0][i] * b) for i in range(3)]
        new_color = color_from_rgb(new_color)
        self.canvas.create_rectangle((x, y)*2, fill=new_color, outline=new_color,
                                     tags=tags,
                                     )

    def set_bw_pixel(self, x: int, y: int, b: float = 1.0, tag: str = None):
        tags = ['drawn']
        if not tag is None:
            tags.append(tag)
        new_color = round(255 * b)
        new_color = color_from_rgb((new_color,new_color,new_color))
        self.canvas.create_rectangle((x, y)*2, fill=new_color, outline=new_color,
                                     tags=tags,
                                     )


class FancyDrawer:
    image: np.ndarray
    _posx: int
    _posy: int
    canvas: tkinter.Canvas

    def __init__(self, path: str, clicked_x: int, clicked_y: int, canv: tkinter.Canvas) -> None:
        im = Image.open("./texture.jpg")
        im.convert('RGB')
        self.image = np.array(im)
        self.x_size = len(self.image[0])
        self.y_size = len(self.image)
        self.img_center = (self.x_size // 2, self.y_size // 2)
        self.clicked_x = clicked_x
        self.clicked_y = clicked_y
        self.canvas = canv

    def set_pixel(self, x, y):
        virt_x = x - self.clicked_x
        virt_y = y - self.clicked_y
        virt_x = (virt_x + self.img_center[0]) % self.x_size
        virt_y = (virt_y + self.img_center[1]) % self.y_size
        rgb = self.image[virt_x][virt_y]
        color = color_from_rgb(rgb)
        self.canvas.create_rectangle(
            (x, y)*2, fill=color, outline=color, tags=['drawn'])

    def draw_line(self, x1, y1, x2, y2):
        while (x1 <= x2):
            self.set_pixel(x1, y1)
            x1 += 1
        print(y1)

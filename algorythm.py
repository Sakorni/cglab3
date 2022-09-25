import numpy as np
import tkinter
from PIL import Image
import math


def _color_from_rgb(color):
    """
    _color_from_rgb convert color from RGB format into friendly to tkinter color
    """
    color = (color[0], color[1], color[2])
    return "#%02x%02x%02x" % color

# def componentToHex(color):
#   var hex = c.toString(16); )))
#   return hex.length == 1 ? "0" + hex : hex;
# :

# def rgbToHex(rgb):
#     return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);


class Booba:
    canvas = None  # That's the current canvas

    def __init__(self, canvas, canvas_color):
        self.canvas = canvas
        self.default_color = canvas_color

    def get_color(self, x, y):
        arr = self.canvas.find_overlapping(x, y, x, y)
        if (len(arr) == 0):
            res = self.default_color
        else:
            res = self.canvas.itemcget(arr[-1], "fill")
        return res

    def isEmptyPixel(self, x, y):
        if (x < 0 or x > self.canvas.winfo_reqwidth()):
            return False
        if (y < 0 or y > self.canvas.winfo_reqheight()):
            return False
        return self.get_color(x, y) == self.empty_color

    def drawLine(self, x1: int, y1: int, x2: int, y2: int):
        """
        drawLine draws a line from x1y1 point to x2y2 point
        """
        self.canvas.create_line(x1, y1, x2, y2,
                                fill=self.active_color[1], capstyle=tkinter.ROUND,
                                smooth=tkinter.TRUE, splinesteps=36, tags=['drawn'])

    def findBorder(self, x: int, y: int, step: int):
        """
        findBorder returns x of last empty pixel
        """
        x += step
        while (self.isEmptyPixel(x, y)):
            x += step
        self.isEmptyPixel(x, y)
        x -= step
        return x

    def fill(self, x: int, y: int, color: tuple):
        self.active_color = color
        self.empty_color = self.get_color(x, y)
        if (self.active_color[1] == self.empty_color):
            return
        self._line_algorithm(x, y, self)
        self.empty_color = None

    def _line_algorithm(self, x: int, y: int, drawer):
        if (not self.isEmptyPixel(x, y)):
            return
        leftBound = self.findBorder(x, y, -1)
        rightBound = self.findBorder(x, y, 1)
        drawer.drawLine(leftBound, y, rightBound + 1, y)
        i = leftBound
        while (i <= rightBound):
            self._line_algorithm(i, y+1, drawer)
            i += 1
        i = leftBound
        while (i <= rightBound):
            self._line_algorithm(i, y-1, drawer)
            i += 1

    def set_pixel(self, x: int, y: int, b: float = 1.0):
        color = [round(self.active_color[0][i] * b) for i in range(3)]
        self.canvas.create_rectangle((x, y)*2, fill=_color_from_rgb(color), outline="",
                                     tags=['drawn', 'line_point'],
                                     )

    def _define_sign(self, d: int) -> int:
        """
        1 - сдвиг слева-направо или сверху-вниз
        -1 - зеркальный сдвиг
        """
        if d > 0:
            return 1
        if d < 0:
            return -1
        return 0

    def bresenham_line(self, color, x1=0, y1=0, x2=0, y2=0):
        self.active_color = color
        dx = x2 - x1  # смещение по x
        dy = y2 - y1  # смещение по y

        sign_x = self._define_sign(dx)
        sign_y = self._define_sign(dy)

        # эквивалент модулю. Мы уже знаем знаки, так что нам не надо их снова вычислять
        dx *= sign_x
        dy *= sign_y
        dl = 0
        dr = 0
        x_addr1, x_addr2, y_addr1, y_addr2 = 0, 0, 0, 0
        if dx == 0:
            gradient = dy
        else:
            gradient = dy/dx

        if gradient <= 1:
            """
            Если dx > dy, то значит отрезок "вытянут" вдоль оси икс, т.е. он скорее длинный, чем высокий.
            Значит в цикле нужно будет идти по икс (строчка el = dx;), значит "протягивать" прямую по иксу
            надо в соответствии с тем, слева направо и справа налево она идёт (pdx = incx;), при этом
            по y сдвиг такой отсутствует.
            """
            dl, dr = dy, dx
            x_addr2, y_addr1 = sign_x, sign_y
            #pdx, pdy = sign_x, 0
            last = dx
        elif gradient > 1:
            dl, dr = dx, dy
            x_addr1, y_addr2 = sign_x, sign_y
            #pdx, pdy = 0, sign_y
            last = dy

        di = 2*dl - dr
        x, y = x1, y1
        t = 0
        self.set_pixel(x, y)  # рисуем первую точку вне цикла

        while t < last:
            if di < 0:
                di += 2*dl
            else:
                y += y_addr1
                x += x_addr1
                di += 2*(dl-dr)
            x += x_addr2
            y += y_addr2
            t += 1
            self.set_pixel(x, y)

    def vu_line(self, color, x1=0, y1=0, x2=0, y2=0):
        self.active_color = color
        self.set_pixel(x1, y1, 1.0)
        dx = x2 - x1
        dy = y2 - y1

        sign_x = self._define_sign(dx)

        dx *= sign_x

        if dx == 0 or dy == 0:
            self.drawLine(x1, y1, x2, y2)
            return
        else:
            gradient = dy / dx

        y = y1 + gradient
        x = x1 + 1
        while (x <= x2 - 1):
            y_frac = y % 1  # fractional part of a number
            self.set_pixel(x, int(y), 1.0 - y_frac)
            self.set_pixel(x, int(y) + 1, y_frac)
            y += gradient
            x += sign_x
            i += 1

    def _1b(self, x, y):
        drawer = FancyDrawer("texture.jpg", self.canvas)
        self.empty_color = self.get_color(x, y)
        self._line_algorithm(x, y, drawer)
        self.empty_color = None


class FancyDrawer:
    image: np.ndarray
    _posx: int
    _posy: int
    canvas: tkinter.Canvas

    def __init__(self, path: str, canv: tkinter.Canvas) -> None:
        im = Image.open("./texture.jpg")
        im.convert('RGB')
        self.image = np.array(im)
        self._posx = 0
        self._posy = 0
        self.canvas = canv

    def drawLine(self, x1, y1, x2, y2):
        while (x1 <= x2):
            if self._posx >= len(self.image):
                self._posx = 0
                self._posy += 1
            if self._posy >= len(self.image[self._posx]):
                self._posy = 0
            color = _color_from_rgb(self.image[self._posx][self._posy])
            self.canvas.create_rectangle((x1, y1)*2, fill=color, outline="",
                                         tags=['drawn'],
                                         )
            self._posx += 1
            x1 += 1
        print(y1)

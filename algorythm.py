import tkinter
from PIL import ImageGrab


class Booba:
    canvas = None  # That's the current canvas
    empty_color: tuple[int] = None  # in RGB format
    fill_color: tuple[int]  # in RGB format

    def __init__(self, canvas):
        self.canvas = canvas
        self.empty_color = (255, 255, 255)

    def _color_from_rgb(self):
        """
        _color_from_rgb convert color from RGB format into friendly to tkinter color
        """
        r, g, b = self.fill_color
        return f'#{r:02x}{g:02x}{b:02x}'

    def update_fill_color(self, color: tuple[int]):
        self.fill_color = color

    def get_color(self, x, y):
        image = ImageGrab.grab((x, y, x+1, y+1))  # 1 pixel image
        return image.getpixel((0, 0))

    def isEmptyPixel(self, x, y):
        return self.get_pixel_color(x, y) == self.empty_color

    def drawLine(self, x1: int, y1: int, x2: int, y2: int):
        """
        drawLine draws a line from x1y1 point to x2y2 point
        """
        self.canvas.create_line(x1, y1, x2, y2,
                                width=self.line_width, fill=self._color_from_rgb(),
                                capstyle=tkinter.ROUND, smooth=tkinter.TRUE, splinesteps=36, tags=['line'])
        print("Woah, line")

    def findBorder(self, x: int, y: int, step: int):
        """
        findBorder returns x of last empty pixel
        """
        while (self.isEmptyPixel(x+step, y)):
            x += step

    def fill(self, x: int, y: int, color: str):
        # color from str
        self.empty_color = self.get_color(x, y)
        self._line_algorithm(x, y)
        self.empty_color = None

    def _line_algorithm(self, x: int, y: int):
        if (not self.isEmptyPixel(x, y)):
            return
        leftBound = self.findBorder(x, y, -1)
        rightBound = self.findBorder(x, y, 1)
        self.drawLine(leftBound, y, rightBound, y)
        i = leftBound
        while (i <= rightBound):
            self._line_algorithm(i, y+1)
            i += 1
        i = leftBound
        while (i <= rightBound):
            self._line_algorithm(i, y-1)
            i += 1

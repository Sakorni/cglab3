from os import curdir
import enum
from additional_classes import *


class Booba:
    canvas = None  # That's the current canvas

    def __init__(self, canvas, canvas_color):
        self.canvas = canvas
        self.color_analyzer = ColorAnalyzer(canvas, canvas_color)

    def findBorder(self, x: int, y: int, step: int, tolerance: int = None):
        """
        findBorder returns x of last empty pixel
        """
        x += step
        while (self.color_analyzer.isEmptyPixel(x, y, tolerance)):
            x += step
        x -= step
        return x

    def fill_with_color(self, x: int, y: int, color: tuple):
        an_color = self.color_analyzer.get_color(x, y)
        self.color_analyzer.set_analyzed_color(an_color)
        if (color == an_color):
            return
        drawer = Drawer(self.canvas, color)
        self._line_algorithm(x, y, drawer)
        self.empty_color = None

    def _line_algorithm(self, x: int, y: int, drawer):
        if (not self.color_analyzer.isEmptyPixel(x, y)):
            return
        leftBound = self.findBorder(x, y, -1)
        rightBound = self.findBorder(x, y, 1)
        drawer.draw_line(leftBound, y, rightBound + 1, y)
        i = leftBound
        while (i <= rightBound):
            self._line_algorithm(i, y+1, drawer)
            i += 1
        i = leftBound
        while (i <= rightBound):
            self._line_algorithm(i, y-1, drawer)
            i += 1

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
        drawer = Drawer(self.canvas, color)
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
        # рисуем первую точку вне цикла
        drawer.set_pixel(x, y, tag='line_point')

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
            drawer.set_pixel(x, y, tag='line_point')

    def vu_line(self, color, x1=0, y1=0, x2=0, y2=0):
        drawer = Drawer(self.canvas, color)
        drawer.set_pixel(x1, y1, 1.0, tag='line_point')
        dx = x2 - x1
        dy = y2 - y1

        sign_x = self._define_sign(dx)

        dx *= sign_x

        if dx == 0 or dy == 0:
            drawer.draw_line(x1, y1, x2, y2, 'line_point')
            return
        else:
            gradient = dy / dx

        y = y1 + gradient
        x = x1 + sign_x
        i = 0
        while (i < dx):
            y_frac = y % 1  # fractional part of a number
            drawer.set_pixel(x, int(y), b=1.0 - y_frac, tag='line_point')
            drawer.set_pixel(x, int(y) + 1, b=y_frac, tag='line_point')
            y += gradient
            x += sign_x
            i += 1

    def fill_with_img(self, x, y):
        drawer = FancyDrawer("texture.jpg", x, y, self.canvas)
        color = self.color_analyzer.get_color(x, y)
        self.color_analyzer.set_analyzed_color(color)
        self._line_algorithm(x, y, drawer)
        self.color_analyzer.set_analyzed_color(None)

    def highlight_border(self, x, y, tolerance = (50, 50, 50)):
        color = self.color_analyzer.get_color(x, y)
        self.color_analyzer.set_analyzed_color(color)
        max_point = [self.findBorder(x, y, step=1, tolerance=tolerance) + 1, y]
        if max_point[0] == -1:
            return
        border_list = list()
        border_list.append(max_point)
        next_point = max_point.copy()
        guard = BorderGuard((x, y), self.color_analyzer, tolerance)
        while(True):
            next_point = guard.next_point(next_point)
            if next_point is None:
                return
            if next_point == max_point:
                break
            border_list.append(next_point)
        color = ((1, 0, 0), 'red')
        drawer = Drawer(self.canvas, color)
        for i in range(len(border_list)):
            drawer.set_pixel(border_list[i][0], border_list[i][1])

        self.color_analyzer.set_analyzed_color(None)

    # def _get_interpolated_line(start_color: tuple, end_color: tuple, coef: int) -> 'tuple[int]':
    #     res = list()
    #     adder = [0.0,0.0,0.0]
    #     for i in range(3):
    #         adder[i] = (end_color[i] - start_color[i]) / (coef - 1)

    #     color = [0.0,0.0,0.0]
    #     for i in range(coef):
    #         for j in range(3):
    #             color[j] = start_color[j] + adder[j] * i
    #         res.append(color.copy())

    #     return res

    # def colorize_triangle(p1, p2, p3):
    #     points = [p1,p2,p3].sort(key=lambda x: x[1])


class Direction(enum.IntEnum):
    right = 0
    up_right = 1
    up = 2
    up_left = 3
    left = 4
    down_left = 5
    down = 6
    down_right = 7


class BorderGuard:

    def __init__(self, start, color_analyzer, tolerance):
        self.start = start
        self.color_analyzer = color_analyzer
        self.tolerance = tolerance
        self.cur_dir = Direction.down
        self.shift_vecs = [(1, 0),     # right
                           (1, -1),    # up right
                           (0, -1),    # up
                           (-1, -1),   # up left
                           (-1, 0),    # left
                           (-1, 1),    # down left
                           (0, 1),     # down
                           (1, 1)      # down_right
                           ]
        self.first = True

    def shift_point(self, point: tuple):
        res = point.copy()
        res[0] += self.shift_vecs[self.cur_dir.value][0]
        res[1] += self.shift_vecs[self.cur_dir.value][1]
        return res

    def _set_90deg_dir(self):
        self.cur_dir = Direction((self.cur_dir.value - 2) % 8)

    def _set_inc_dir(self):
        self.cur_dir = Direction((self.cur_dir.value + 1) % 8)

    def next_point(self, point: tuple):
        if self.first:
            self.first = False
            next_point = self.shift_point(point)
            if not self.color_analyzer.isEmptyPixel(next_point[0], next_point[1],
                                                    tolerance=self.tolerance):
                return next_point

        self._set_90deg_dir()
        temp_dir = self.cur_dir
        while True:
            next_point = self.shift_point(point)
            if not self.color_analyzer.isEmptyPixel(next_point[0], next_point[1],
                                                    tolerance=self.tolerance):
                return next_point
            self._set_inc_dir()
            if temp_dir == self.cur_dir:
                self.cur_dir = temp_dir
                return None

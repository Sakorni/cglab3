
from turtle import right
from additional_classes import Drawer, color_from_hex


class TriangleVert:
    x: int
    y: int
    color: tuple[tuple[int], str]

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color_from_hex(color)


class TriangleAlgorythm():
    verts: list[TriangleVert]
    drawer: Drawer

    def __init__(self, verts: list[int], drawer: Drawer) -> None:
        if (len(verts) != 3):
            print("R U MAD?????")
            raise Exception("Invalid number of triangle verts")
        self.verts = []
        for i in verts:
            self.verts.append(TriangleVert(i[0], i[1], i[2]))
        self.drawer = drawer
        self.order_verts_by_y()

    def do_the_trick(self):
        line1 = self.get_line_coordinates(
            self.verts[0].x, self.verts[0].y, self.verts[1].x, self.verts[1].y)
        line2 = self.get_line_coordinates(
            self.verts[1].x, self.verts[1].y, self.verts[2].x, self.verts[2].y)
        line3 = self.get_line_coordinates(
            self.verts[0].x, self.verts[0].y, self.verts[2].x, self.verts[2].y)
        color1 = self.rgb_interpolate(
            color1=self.verts[0].color, color2=self.verts[1].color, seed=len(line1))
        color2 = self.rgb_interpolate(
            color1=self.verts[1].color, color2=self.verts[2].color, seed=len(line2))
        color3 = self.rgb_interpolate(
            color1=self.verts[0].color, color2=self.verts[2].color, seed=len(line3))

        for p in line1:
            self.drawer.set_colored_pixel(p[0], p[1], [0, 0, 0])
        for p in line2:
            self.drawer.set_colored_pixel(p[0], p[1], [0, 0, 0])
        for p in line3:
            self.drawer.set_colored_pixel(p[0], p[1], [0, 0, 0])
        i = 0
        i1 = 0
        y = -1
        while (y < self.verts[1].y):
            y = line1[i][1]
            x1 = line1[i][0]

            y2 = line3[i1][1]
            while y2 < y:
                i1 += 1
                y2 = line3[i1][1]

            x2 = line3[i1][0]
            colors = []
            left_x, right_x = x1, x2
            if left_x > right_x:
                left_x, right_x = x2, x1
                colors = self.rgb_interpolate(
                    color3[i1], color1[i], abs(x1-x2)+1)
            else:
                colors = self.rgb_interpolate(
                    color1[i], color3[i1], abs(x1-x2)+1)

            j = 0
            while (left_x <= right_x):
                self.drawer.set_colored_pixel(left_x, y, colors[j])
                left_x += 1
                j += 1

            i += 1

        i = 0
        y = -1
        while (y < self.verts[2].y):
            if y == line2[i][1]:
                i += 1
                continue
            y = line2[i][1]
            x1 = line2[i][0]
            y2 = line3[i1][1]
            while y2 < y:
                i1 += 1
                y2 = line3[i1][1]

            x2 = line3[i1][0]
            colors = []
            left_x = x1
            right_x = x2
            if left_x > right_x:
                right_x, left_x = left_x, right_x
                colors = self.rgb_interpolate(
                    color3[i1], color2[i], abs(x1-x2)+1)
            else:
                colors = self.rgb_interpolate(
                    color2[i], color3[i1], abs(x1-x2)+1)
            j = 0
            while (left_x <= right_x):
                self.drawer.set_colored_pixel(left_x, y, colors[j])
                left_x += 1
                j += 1
            i += 1

    def rgb_interpolate(self, color1: list[int], color2: list[int], seed: int):
        """
        rgb_interpolate returns the list of interpolated colors for {seed} number of points
        """
        res = []
        steps = [0, 0, 0]
        for i in range(len(color1)):
            delim = (1.0*seed - 1)
            if delim == 0:
                delim = 1
            steps[i] = round(color2[i] + (color1[i]-color2[i]) / delim)
        for i in range(seed):
            color = []
            for j in range(len(color1)):
                color.append((color1[j] + steps[j]*i) % 256)
            res.append(color)
        return res

    def order_verts_by_y(self):
        self.verts.sort(key=lambda x: x.y)

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

    def get_line_coordinates(self, x1: int, y1: int, x2: int, y2: int) -> list[list[int]]:
        res = []
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
            dl, dr = dy, dx
            x_addr2, y_addr1 = sign_x, sign_y
            # pdx, pdy = sign_x, 0
            last = dx
        elif gradient > 1:
            dl, dr = dx, dy
            x_addr1, y_addr2 = sign_x, sign_y
            # pdx, pdy = 0, sign_y
            last = dy

        di = 2*dl - dr
        x, y = x1, y1
        t = 0
        # рисуем первую точку вне цикла
        res.append([x, y])

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
            res.append([x, y])
        return res

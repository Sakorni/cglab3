from tkinter import *
from tkinter.colorchooser import askcolor
from additional_classes import Drawer
from algorythm import Booba
from triangle_algorythm import TriangleAlgorythm, TriangleVert


class Paint(object):
    DEFAULT_CANVAS_COLOR = ((1.0, 1.0, 1.0), 'white')
    W_SIZE = 600
    points = [
        [100, 400, '#FF0000'],
        [100, 100, '#00FF00'],
        [500, 442, '#0000FF']]
    point_number = 0
    mode = 0
    c: Canvas = None

    def __init__(self):
        self.root = Tk()
        self.mode = 1
        self.fpoint_c_button = Button(
            self.root, text='First point color', command=lambda: self.choose_color(0))
        self.fpoint_c_button.grid(row=0, column=0)

        self.spoint_c_button = Button(
            self.root, text='Second point color', command=lambda: self.choose_color(1))
        self.spoint_c_button.grid(row=0, column=1)

        self.tpoint_c_button = Button(
            self.root, text='Third point color', command=lambda: self.choose_color(2))
        self.tpoint_c_button.grid(row=0, column=2)

        self.draw_button = Button(
            self.root, text='Draw', command=lambda: self.draw())
        self.draw_button.grid(row=0, column=3)

        self.c = Canvas(self.root, bg='white',
                        width=self.W_SIZE, height=self.W_SIZE)
        self.c.grid(row=1, columnspan=4)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.c.bind('<B1-Motion>', self.on_motion)
        self.c.bind('<ButtonPress-1>', self.on_press)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.filler = Booba(self.c, self.DEFAULT_CANVAS_COLOR[1])
        self.draw_points()
        # self.draw()

    def choose_color(self, point_n):
        c = askcolor(color=self.points[point_n][2])
        if not (c[1] is None):
            self.points[point_n][2] = c[1]
            self.c.delete("all")
            self.draw_points()

    def draw_points(self):
        for i in range(len(self.points)):
            self.c.create_oval(self.points[i][0], self.points[i][1],
                               self.points[i][0] +
                               10.0, self.points[i][1] + 10.0,
                               fill=self.points[i][2])

    def activate_button(self, btn_to_act):
        self.active_button.config(relief=RAISED)
        btn_to_act.config(relief=SUNKEN)
        self.active_button = btn_to_act

    def on_motion(self, event):
        if self.mode == 0:
            self.line_width = self.choose_size_button.get()
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=self.color[1],
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36, tags=['drawn'])

            self.old_x = event.x
            self.old_y = event.y

    def on_press(self, event):
        if self.mode == 1:
            self.set_point(event.x, event.y)
            return
        if self.mode == 2:
            self.filler._1b(event.x, event.y)
            return

    def set_point(self, x, y):
        point = self.points[self.point_number]
        self.points[self.point_number] = [x, y, point[2]]
        self.point_number = (self.point_number + 1) % 3
        self.clear_canvas()
        self.draw_points()

    def draw(self):
        alg = TriangleAlgorythm(self.points, Drawer(
            self.c, self.DEFAULT_CANVAS_COLOR))
        alg.do_the_trick()

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clear_canvas(self):
        self.c.delete('all')


if __name__ == '__main__':
    Paint()

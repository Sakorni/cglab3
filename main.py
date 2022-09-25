from tkinter import *
from tkinter.colorchooser import askcolor
from algorythm import Booba


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_PEN_COLOR = ((0.0, 0.0, 0.0), 'black')
    DEFAULT_CANVAS_COLOR = ((1.0, 1.0, 1.0), 'white')
    W_SIZE = 600
    fill_mode = False

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.pen_mode)
        self.pen_button.grid(row=0, column=0)

        self.fill_button = Button(
            self.root, text='fill', command=self.fill_mode)
        self.fill_button.grid(row=0, column=1)

        self.fill_file_button = Button(
            self.root, text='fill with img', command=self.fill_with_img_mode)
        self.fill_file_button.grid(row=0, column=2)

        self.br_line_button = Button(
            self.root, text='Bresenham line', command=self.br_line_mode)
        self.br_line_button.grid(row=0, column=3)

        self.vu_line_button = Button(
            self.root, text='VU line', command=self.vu_line_mode)
        self.vu_line_button.grid(row=0, column=4)

        self.color_button = Button(
            self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=5)

        self.reset_button = Button(
            self.root, text='clear', command=self.clear_canvas)
        self.reset_button.grid(row=0, column=6)

        self.choose_size_button = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=7)

        self.c = Canvas(self.root, bg='white',
                        width=self.W_SIZE, height=self.W_SIZE)
        self.c.grid(row=1, columnspan=8)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_PEN_COLOR
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.on_motion)
        self.c.bind('<ButtonPress-1>', self.on_press)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.filler = Booba(self.c, self.DEFAULT_CANVAS_COLOR[1])
        self.mode = None

    def pen_mode(self):
        self.activate_button(self.pen_button)
        self.mode = 0

    def fill_mode(self):
        self.activate_button(self.fill_button)
        self.mode = 1

    def fill_with_img_mode(self):
        self.activate_button(self.fill_file_button)
        self.mode = 2

    def br_line_mode(self):
        self.activate_button(self.br_line_button)
        self.mode = 3

    def vu_line_mode(self):
        self.activate_button(self.vu_line_button)
        self.mode = 4

    def choose_color(self):
        c = askcolor(color=self.color[1])
        if not (c[0] is None):
            self.color = c

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
            self.filler.fill(event.x, event.y, self.color)
            return
        if self.mode == 2:
            self.filler._1b(event.x, event.y)
            return

        if self.mode == 3 or self.mode == 4:
            points = self.c.find_withtag("point")
            if len(points) == 0:
                self.c.create_oval(event.x, event.y, event.x + 5.0, event.y + 5.0,
                                   fill=self.color[1], tags=['drawn', 'point'])
                return
            if len(points) == 2:
                self.c.delete(points[0])
                self.c.delete("line_point")

            self.c.create_oval(event.x, event.y, event.x + 5.0, event.y + 5.0,
                               fill=self.color[1], tags=['drawn', 'point'])
            points = self.c.find_withtag("point")
            xy1 = self.c.coords(points[0])
            xy2 = self.c.coords(points[1])
            self.filler.bresenham_line(
                self.color, xy1[0], xy1[1], xy2[0], xy2[1])

            return

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clear_canvas(self):
        self.c.delete('drawn')

    def draw_test_square(self):
        self.c.create_line(20, 20, 80, 20)
        self.c.create_line(20, 20, 20, 80)
        self.c.create_line(20, 80, 80, 80)
        self.c.create_line(80, 20, 80, 80)

    def draw_test_square(self):
        self.c.create_line(20, 20, 80, 20)
        self.c.create_line(20, 20, 20, 80)
        self.c.create_line(20, 80, 80, 80)
        self.c.create_line(80, 20, 80, 80)


if __name__ == '__main__':
    Paint()

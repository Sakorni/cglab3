from tkinter import *
from tkinter.colorchooser import askcolor
from algorythm import Booba


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_PEN_COLOR = ((0.0, 0.0, 0.0), '#000000')
    DEFAULT_CANVAS_COLOR = ((1.0, 1.0, 1.0), '#ffffff')
    W_SIZE = 600
    fill_mode = False

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(
            self.root, text='pen', command=lambda: self.set_mode(0))
        self.pen_button.grid(row=0, column=0)

        self.fill_button = Button(
            self.root, text='fill', command=lambda: self.set_mode(1))
        self.fill_button.grid(row=0, column=1)

        self.fill_file_button = Button(
            self.root, text='fill with img', command=lambda: self.set_mode(2))
        self.fill_file_button.grid(row=0, column=2)

        self.highlight_border_btn = Button(
            self.root, text='Highlight border', command=lambda: self.set_mode(3))
        self.highlight_border_btn.grid(row=0, column=3)

        self.br_line_button = Button(
            self.root, text='Bresenham line', command=lambda: self.set_mode(4))
        self.br_line_button.grid(row=0, column=4)

        self.vu_line_button = Button(
            self.root, text='VU line', command=lambda: self.set_mode(5))
        self.vu_line_button.grid(row=0, column=5)

        self.color_button = Button(
            self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=6)

        self.reset_button = Button(
            self.root, text='clear', command=self.clear_canvas)
        self.reset_button.grid(row=0, column=7)

        self.choose_size_button = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=8)

        self.c = Canvas(self.root, bg='#ffffff',
                        width=self.W_SIZE, height=self.W_SIZE)
        self.c.grid(row=1, columnspan=9)

        self.img = PhotoImage(width=self.W_SIZE, height=self.W_SIZE)
        self.c.create_image((self.W_SIZE/2, self.W_SIZE/2), image=self.img, 
                            state='normal', tags=['canvas'])

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

    def set_mode(self, n):
        self.mode = n
        if n == 0:
            self.activate_button(self.pen_button)
        elif n == 1:
            self.activate_button(self.fill_button)
        elif n == 2:
            self.activate_button(self.fill_file_button)
        elif n == 3:
            self.activate_button(self.highlight_border_btn)
        elif n == 4:
            self.activate_button(self.br_line_button)
        else:
            self.activate_button(self.vu_line_button)

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
            self.filler.fill_with_color(event.x, event.y, self.color)
            return
        if self.mode == 2:
            self.filler.fill_with_img(event.x, event.y)
            return

        if self.mode == 3:
            self.filler.highlight_border(
                event.x, event.y, highlight_color=self.color)
            return

        if self.mode == 4 or self.mode == 5:
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
            if self.mode == 4:
                self.filler.bresenham_line(
                    self.color, xy1[0], xy1[1], xy2[0], xy2[1])
            else:
                self.filler.right_wu_line(
                    self.color, xy1[0], xy1[1], xy2[0], xy2[1])

            return

    def create_square(self):
        self.line_width = self.choose_size_button.get()
        points = [(20, 20), (40, 20), (20, 40), (40, 40)]
        self.c.create_line(
            points[0], points[1], width=self.line_width, fill='#000000', tags=['drawn'])
        self.c.create_line(
            points[0], points[2], width=self.line_width, fill='#000000', tags=['drawn'])
        self.c.create_line(
            points[1], points[3], width=self.line_width, fill='#000000', tags=['drawn'])
        self.c.create_line(
            points[2], points[3], width=self.line_width, fill='#000000', tags=['drawn'])

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def clear_canvas(self):
        self.c.delete('drawn')


if __name__ == '__main__':
    Paint()

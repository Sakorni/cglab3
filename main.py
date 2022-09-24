from tkinter import *
from tkinter.colorchooser import askcolor
import turtle


class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    W_SIZE = 600

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.color_button = Button(
            self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=1)

        self.reset_button = Button(
            self.root, text='reset', command=self.reset)
        self.reset_button.grid(row=0, column=2)

        self.choose_size_button = Scale(
            self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=3)

        self.c = Canvas(self.root, bg='white',
                        width=self.W_SIZE, height=self.W_SIZE)
        self.c.grid(row=1, columnspan=4)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = 'black'
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.color = askcolor(color=self.color)[1]

    def activate_button(self, btn_to_act):
        self.active_button.config(relief=RAISED)
        btn_to_act.config(relief=SUNKEN)
        self.active_button = btn_to_act

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=self.color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36, tags=['line'])

        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None
        self.c.delete('line')

    def get_pixel_color(x, y):
        y = -y

        # get access to tkinter.Canvas
        canvas = turtle.getcanvas()

        # find IDs of all objects in rectangle (x, y, x, y)
        ids = canvas.find_overlapping(x, y, x, y)

        # if found objects
        if ids:
            # get ID of last object (top most)
            index = ids[-1]

            # get its color
            color = canvas.itemcget(index, "fill")

            # if it has color then return it
            if color:
                return color

        # if there was no object then return "white" - background color in turtle
        return "white"  # default color


if __name__ == '__main__':
    Paint()

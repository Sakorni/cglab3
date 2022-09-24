import turtle


class Booba:
    canvas = None  # That's the current canvas
    visitedY = set()

    def get_pixel_color(self, x, y):
        y = -y

        # get access to tkinter.Canvas
        #canvas = turtle.getcanvas()
        canvas = self.canvas

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

    def isEmptyPixel(self, x, y):
        return self.get_pixel_color(x, y) == "white"

    def drawLine(self, x1: int, y1: int, x2: int, y2: int):
        """
        drawLine draws a line from x1y1 point to x2y2 point
        """
        self.canvas.create_line(x1, y1, x2, y2,
                                width=self.line_width, fill=self.color,
                                capstyle=ROUND, smooth=TRUE, splinesteps=36, tags=['line'])
        print("Woah, line")

    def findBorder(self, x: int, y: int, step: int):
        """
        findBorder returns x of last empty pixel
        """
        while (self.isEmptyPixel(x+step, y)):
            x += step

    def line_algorithm(self, x: int, y: int):
        if (not self.isEmptyPixel(x, y)):
            return
        leftBound = self.findBorder(x, y, -1)
        rightBound = self.findBorder(x, y, 1)
        self.drawLine(leftBound, y, rightBound, y)
        i = leftBound
        while (i <= rightBound):
            self.line_algorithm(i, y+1)
            i += 1
        i = leftBound
        while (i <= rightBound):
            self.line_algorithm(i, y-1)
            i += 1

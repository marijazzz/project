from tkinter import *
import math


class Paint(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.n = 1
        self.red, self.green, self.blue = 0, 0, 0
        self.parent = parent
        self.color = "black"
        self.color_canvas = "white"
        self.brush_size = 2
        self.setUI()
        self.file_name = 'untitled'
        self.type = 'circle'

    def set_color(self):
        red, green, blue = int(self.scale_red.get()), int(self.scale_green.get()), int(self.scale_blue.get())
        tk_rgb = "#%02x%02x%02x" % (red, green, blue)
        self.color = tk_rgb

    def set_color_canvas(self):
        red, green, blue = int(self.scale_red.get()), int(self.scale_green.get()), int(self.scale_blue.get())
        tk_rgb = "#%02x%02x%02x" % (red, green, blue)
        self.color_canvas = tk_rgb
        self.canv.config(bg = self.color_canvas)
        self.parent.update_idletasks()

    def symmetry(self):
        n = int(self.scale_symmetry.get())
        self.n = n

    def draw(self, event):
        if self.type == 'circle':
            self.draw_circle(event)
        if self.type == 'triangle':
            self.draw_triangle(event)
        if self.type == 'rectangle':
            self.draw_rectangle(event)

    def draw_triangle(self, event):
        self.canvas_width_center = self.canv.winfo_width() / 2
        self.canvas_heigt_center = self.canv.winfo_height() / 2
        x = event.x - self.canvas_width_center
        y = -event.y + self.canvas_heigt_center
        l = math.sqrt(x ** 2 + y ** 2)
        if y == 0:
            phi = math.pi / 2
        else:
            phi = math.atan2(x, y)
        for i in range(self.n):
            self.parent.update_idletasks()
            alpha = phi + i / self.n * 2 * math.pi
            x_polar = l * math.sin(alpha) + self.canvas_width_center
            y_polar = -l * math.cos(alpha) + self.canvas_heigt_center
            self.canv.create_polygon(x_polar, y_polar + 1, x_polar + 1,
                                  y_polar - 1, x_polar - 1,
                                  y_polar - 1, fill=self.color, outline=self.color)

    def draw_rectangle(self, event):
        self.canvas_width_center = self.canv.winfo_width() / 2
        self.canvas_heigt_center = self.canv.winfo_height() / 2
        x = event.x - self.canvas_width_center
        y = -event.y + self.canvas_heigt_center
        l = math.sqrt(x ** 2 + y ** 2)
        if y == 0:
            phi = math.pi / 2
        else:
            phi = math.atan2(x, y)
        for i in range(self.n):
            self.parent.update_idletasks()
            alpha = phi + i / self.n * 2 * math.pi
            x_polar = l * math.sin(alpha) + self.canvas_width_center
            y_polar = -l * math.cos(alpha) + self.canvas_heigt_center
            self.canv.create_rectangle(x_polar - 5, y_polar -5, x_polar + 5,
                                  y_polar + 5,  width = 5, fill=self.color, outline=self.color)

    def draw_circle(self, event):
        self.canvas_width_center = self.canv.winfo_width() / 2
        self.canvas_heigt_center = self.canv.winfo_height() / 2
        x = event.x - self.canvas_width_center
        y = -event.y + self.canvas_heigt_center
        l = math.sqrt(x ** 2 + y ** 2)
        if y == 0:
            phi = math.pi / 2
        else:
            phi = math.atan2(x, y)
        for i in range(self.n):
            self.parent.update_idletasks()
            alpha = phi + i / self.n * 2 * math.pi
            x_polar = l * math.sin(alpha) + self.canvas_width_center
            y_polar = -l * math.cos(alpha) + self.canvas_heigt_center
            self.canv.create_oval(x_polar - 1, y_polar - 1, x_polar + 1,
                                  y_polar + 1, fill=self.color, outline=self.color)

    def file_save(self):
        self.file_name = self.e.get()
        self.canv.postscript(file = self.file_name, colormode = 'color')


    def setUI(self):
        self.parent.title("рисовалка")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(9, weight=1)
        self.rowconfigure(2, weight=1)

        for i in range(8):
            self.grid_columnconfigure(i, minsize = 100)

        self.canv = Canvas(self, bg=self.color_canvas)
        self.canv.grid(row=2, column=0, columnspan=10, padx=5, pady=5, sticky=E + W + S + N)
        self.canv.bind("<B1-Motion>", self.draw)

        color_setting_btn = Button(self, text="Set color", width=10,command=lambda: self.set_color())
        color_setting_btn.grid(row=0, column=6)

        color_setting_btn = Button(self, text="Set canvas color", width=14, command=lambda: self.set_color_canvas())
        color_setting_btn.grid(row=0, column=8)

        self.scale_red = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_red.grid(row=0, column=0)
        label_red = Label(self, text='Red')
        label_red.grid(row = 0, column = 1)

        self.scale_green = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_green.grid(row=0, column=2)
        label_green = Label(self, text='Green')
        label_green.grid(row=0, column=3)

        self.scale_blue = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_blue.grid(row=0, column=4)
        label_blue = Label(self, text='Blue')
        label_blue.grid(row=0, column=5)

        size_lab = Label(self, text="Symmetry number")
        size_lab.grid(row=1, column=0, padx=6)
        self.scale_symmetry = Scale(self, from_= 1, to=10, orient=HORIZONTAL)
        self.scale_symmetry.grid(row=1, column=1)

        self.scale_blue = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_blue.grid(row=0, column=4)
        self.label_blue = Label(self, text='Blue')
        self.label_blue.grid(row=0, column=5)

        get_symmetry_btn = Button(self, text="Set symmetry number", width=16, command=lambda: self.symmetry())
        get_symmetry_btn.grid(row=1, column=2)

        clean_btn = Button(self, text="Clean", width=5, command=lambda: self.canv.delete('all'))
        clean_btn.grid(row=0, column=7)

        Label(self, text="File name").grid(row=1, column = 3)
        self.e = Entry(self)
        self.e.grid(row=1, column=4)
        self.e.insert(10,"Untitled")

        file_btn = Button(self, text="Save", width=5, command=lambda: self.file_save())
        file_btn.grid(row=1, column=5)

        circle_btn = Button(self, text="Draw circlesr", width=14, command=lambda: self.set_type('circle'))
        circle_btn.grid(row=1, column=6)

        triangle_btn = Button(self, text="Draw triangles", width=14, command=lambda: self.set_type('triangle'))
        triangle_btn.grid(row=1, column=7)

        rectangle_btn = Button(self, text="SDraw rectangles", width=14, command=lambda: self.set_type('rectangle'))
        rectangle_btn.grid(row=1, column=8)

    def set_type(self, n):
        if n == 'circle':
            self.type = 'circle'
        if n == 'triangle':
            self.type = 'triangle'
        if n == 'rectangle':
            self.type = 'rectangle'
if __name__ == '__main__':
    root = Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    app = Paint(root)
    root.mainloop()
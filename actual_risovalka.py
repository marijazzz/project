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

    def set_color(self):
        red, green, blue = self.getting_values()
        tk_rgb = "#%02x%02x%02x" % (red, green, blue)
        self.color = tk_rgb

    def set_color_canvas(self):
        red, green, blue = self.getting_values()
        tk_rgb = "#%02x%02x%02x" % (red, green, blue)
        self.color_canvas = tk_rgb
        self.canv(bg = self.color_canvas)
    def symmetry(self, n):
        self.n = n

    def draw(self, event):
        self.canvas_width_center = self.canv.winfo_width() / 2
        self.canvas_heigt_center = self.canv.winfo_height() / 2
        x = event.x - self.canvas_width_center
        y = -event.y + self.canvas_heigt_center
        l = math.sqrt(x**2 + y**2)
        if y == 0:
            phi = math.pi/2
        else:
            phi = math.atan2(x, y)
        for i in range(self.n):
            self.parent.update_idletasks()
            alpha = phi + i / self.n * 2 * math.pi
            x_polar = l * math.sin(alpha) + self.canvas_width_center
            y_polar = -l * math.cos(alpha) + self.canvas_heigt_center
            self.canv.create_oval(x_polar - 1, y_polar - 1, x_polar + 1,
                                  y_polar + 1, fill=self.color, outline=self.color)




    def setUI(self):
        self.parent.title("рисовалка")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(7, weight=1)
        self.rowconfigure(2, weight=1)

        for i in range(8):
            self.grid_columnconfigure(i, minsize = 100)

        self.canv = Canvas(self, bg=self.color_canvas)
        self.canv.grid(row=2, column=0, columnspan=8, padx=5, pady=5, sticky=E + W + S + N)
        self.canv.bind("<B1-Motion>", self.draw)


        self.color_setting_btn = Button(self, text="Set color", width=10,command=lambda: self.set_color())
        self.color_setting_btn.grid(row=0, column=6)

        self.scale_red = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_red.grid(row=0, column=0)
        self.label_red = Label(self, text='Red')
        self.label_red.grid(row = 0, column = 1)

        self.scale_green = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_green.grid(row=0, column=2)
        self.label_green = Label(self, text='Green')
        self.label_green.grid(row=0, column=3)

        self.scale_blue = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_blue.grid(row=0, column=4)
        self.label_blue = Label(self, text='Blue')
        self.label_blue.grid(row=0, column=5)

        size_lab = Label(self, text="Symmetry ")
        size_lab.grid(row=1, column=0, padx=6)

        self.one_btn = Button(self, text="one", width=5, command=lambda: self.symmetry(1))
        self.one_btn.grid(row=1, column=1)

        self.two_btn = Button(self, text="two", width=5, command=lambda: self.symmetry(2))
        self.two_btn.grid(row=1, column=2)

        self.three_btn = Button(self, text="three", width=5, command=lambda: self.symmetry(3))
        self.three_btn.grid(row=1, column=3)

        self.four_btn = Button(self, text="four", width=5, command=lambda: self.symmetry(4))
        self.four_btn.grid(row=1, column=4)

        self.five_btn = Button(self, text="five", width=5, command=lambda: self.symmetry(5))
        self.five_btn.grid(row=1, column=5)

        self.six_btn = Button(self, text="six", width=5, command=lambda: self.symmetry(6))
        self.six_btn.grid(row=1, column=6)

        self.seven_btn = Button(self, text="seven", width=5, command=lambda: self.symmetry(7))
        self.seven_btn.grid(row=1, column=7)

        self.clean_btn = Button(self, text="Clean", width=5, command=lambda: self.canv.delete('all'))
        self.clean_btn.grid(row=0, column=7)

    def getting_values(self):
        self.red, self.green, self.blue = int(self.scale_red.get()), int(self.scale_green.get()), int(self.scale_blue.get())
        return self.red, self.green, self.blue

if __name__ == '__main__':
    root = Tk()
    root.geometry("800x800")
    app = Paint(root)
    root.mainloop()
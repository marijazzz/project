from tkinter import *
import math
class Paint(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.n = 2
        self.parent = parent
        self.color = "black"
        self.brush_size = 2
        self.setUI()

    def set_color(self, tk_rgb):
        self.color = tk_rgb

    def set_brush_size(self, new_size):
        self.brush_size = new_size
    def colors(self):
        tk_rgb = "#%02x%02x%02x" % (self.red, self.green, self.blue)
        return(tk_rgb)
    def symmetry(self, n):
        self.n = n
        self.angle = math.pi/n

    def draw(self, event):
        x = event.x - 100
        y = event.y - 100
        l = math.sqrt(x**2 + y**2)
        phi = math.asin(x / l)
        for i in range(self.n):
            alpha = phi + i / self.n * 2 * math.pi
            x_polar = l * math.sin(alpha)
            y_polar = l * math.cos(alpha)
            self.canv.create_oval(x_polar - 1, y_polar - 1, x_polar + 1,
                              y_polar + 1, fill=self.color, outline=self.color)



    def setUI(self):
        self.parent.title("рисовалка")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(6, weight=1)
        self.rowconfigure(2, weight=1)

        self.canv = Canvas(self, bg="white", width=200, height=200)
        self.canv.grid(row=2, column=0)
        self.canv.bind("<B1-Motion>", self.draw)

        two_btn = Button(self, text="two", width=10,command=lambda: self.symmetry(2))
        two_btn.grid(row=1, column=1)

        scale_red = Scale(self, from_=0, to=255)
        scale_red.grid(row=0, column=0)
        self.var_red = IntVar()
        self.label_red = Label(self, text='Red')
        self.label_red.grid(row = 0, column = 1)
        scale_green = Scale(self, from_=0, to=255)
        scale_green.grid(row=0, column=2)
        self.var_green = IntVar()
        self.label_green = Label(self, text='Green')
        self.label_green.grid(row=0, column=3)
        scale_blue = Scale(self, from_=0, to=255)
        scale_blue.grid(row=0, column=4)
        self.var_blue = IntVar()
        self.label_blue = Label(self, text='Blue')
        self.label_blue.grid(row=0, column=5)
        self.red, self.blue, self.green = int(scale_red.get()), int(scale_green.get()), int(scale_blue.get())

        print(self.red)
if __name__ == '__main__':
    root = Tk()
    root.geometry("500x500")
    app = Paint(root)
    root.mainloop()
from tkinter import *
from math import pi, cos, sin, sqrt, atan2
from PIL import ImageGrab


class Paint(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.n = 1  # Колличество симметрий
        self.red, self.green, self.blue = 0, 0, 0  # Цвета в формате RGB
        self.parent = parent  # Родитель
        self.color = "black"  # Цвет рисуемых фигур
        self.color_canvas = "white"  # Цвет canvas
        self.file_name = 'Untitled'  # Имя файла
        self.type = 'circle'  # Тип рисуемой фигуры
        self.brush_size = 1  # Размер кисти
        self.canvas_width_center = 0  # Центр по ширине canvas
        self.canvas_height_center = 0  # Центр по высоте canvas
        self.set_ui()  # Вызов функции задания виджитов

        '''Задаем основные переменные, используемые сразу в нескольких функциях,
        вызываем рабучую функцию, которая задает все виджеты нашего приложегния. 
        '''

    def set_color_canvas(self):
        self.color_canvas = "#%02x%02x%02x" % (int(self.scale_red.get()),
                                               int(self.scale_green.get()),
                                               int(self.scale_blue.get()))
        # Получаем цвет в нужном нам формате.
        self.canvas.config(bg=self.color_canvas)
        ''' Функция, меняющая цвет canvas. 
        
        '''

    def draw(self, event):
        self.n = int(self.scale_symmetry.get())
        self.color = "#%02x%02x%02x" % (int(self.scale_red.get()),
                                        int(self.scale_green.get()),
                                        int(self.scale_blue.get()))
        self.brush_size = int(self.scale_brush.get())/2
        # Задаем количество симметрий n, цвет для рисования и размер кисти.
        if self.type == 'circle':
            self.draw_circle(event)
        if self.type == 'triangle':
            self.draw_triangle(event)
        if self.type == 'rectangle':
            self.draw_rectangle(event)

        print(self.type)
        # Разделение по типам рисуемой фигуры.
        '''
        Получаем размер и цвет рисуемых фигур, их тип
        '''

    def draw_triangle(self, event):  # Функция рисования треугольников
        self.canvas_width_center = self.canvas.winfo_width() / 2
        self.canvas_height_center = self.canvas.winfo_height() / 2
        x = event.x - self.canvas_width_center
        y = -event.y + self.canvas_height_center
        # Рассчет для перехода в систему координат в центре self.canvas.
        radius = sqrt(x ** 2 + y ** 2)
        # Радиус-вектор для перехода в полярную СК.
        if y == 0:
            phi = pi / 2
        else:
            phi = atan2(x, y)
        # Рассчет угла для перехода в полярную СК.
        for i in range(self.n):  # Рисование симметрично.
            self.parent.update_idletasks()
            # Обновление canvas.
            alpha = phi + i / self.n * 2 * pi
            # Угол в полярной СК в зависимости от количества симметий.
            x_polar = radius * sin(alpha) + self.canvas_width_center
            y_polar = -radius * cos(alpha) + self.canvas_height_center
            # Переход из полярной СК в СК экрана.
            self.canvas.create_polygon(x_polar, y_polar + self.brush_size, x_polar + self.brush_size,
                                       y_polar - self.brush_size, x_polar - self.brush_size,
                                       y_polar - self.brush_size, fill=self.color, outline=self.color)
            # Рисование треугольника.
    '''
    Отрисовка треугольников
    '''

    def draw_rectangle(self, event):  # Функция для рисования квадратов.
        self.canvas_width_center = self.canvas.winfo_width() / 2
        self.canvas_height_center = self.canvas.winfo_height() / 2
        x = event.x - self.canvas_width_center
        y = -event.y + self.canvas_height_center
        # Рассчет для перехода в систему координат в центре self.canvas.
        radius = sqrt(x ** 2 + y ** 2)
        # Радиус-вектор для перехода в полярную СК.
        if y == 0:
            phi = pi / 2
        else:
            phi = atan2(x, y)
        # Рассчет угла для перехода в полярную СК.
        for i in range(self.n):  # Рисование симметрично.
            self.parent.update_idletasks()
            # Обновление canvas.
            alpha = phi + i / self.n * 2 * pi
            # Угол в полярной СК в зависимости от количества симметий.
            x_polar = radius * sin(alpha) + self.canvas_width_center
            y_polar = -radius * cos(alpha) + self.canvas_height_center
            # Переход из полярной СК в СК экрана.
            self.canvas.create_rectangle(x_polar - self.brush_size, y_polar - self.brush_size,
                                         x_polar + self.brush_size, y_polar + self.brush_size,
                                         fill=self.color, outline=self.color)
            # Рисование квадрата.
    '''
    Отрисовка квадратов
    '''

    def draw_circle(self, event):  # Функция для рисования кругов.
        self.canvas_width_center = self.canvas.winfo_width() / 2
        self.canvas_height_center = self.canvas.winfo_height() / 2
        x = event.x - self.canvas_width_center
        y = -event.y + self.canvas_height_center
        # Рассчет для перехода в систему координат в центре self.canvas.
        radius = sqrt(x ** 2 + y ** 2)
        # Радиус-вектор для перехода в полярную СК.
        if y == 0:
            phi = pi / 2
        else:
            phi = atan2(x, y)
        # Рассчет угла для перехода в полярную СК.
        for i in range(self.n):  # Рисование симметрично.
            self.parent.update_idletasks()
            # Обновление canvas.
            alpha = phi + i / self.n * 2 * pi
            # Угол в полярной СК в зависимости от количества симметий.
            x_polar = radius * sin(alpha) + self.canvas_width_center
            y_polar = -radius * cos(alpha) + self.canvas_height_center
            # Переход из полярной СК в СК экрана.
            self.canvas.create_oval(x_polar - self.brush_size, y_polar - self.brush_size,
                                    x_polar + self.brush_size, y_polar + self.brush_size,
                                    fill=self.color, outline=self.color)
            # Рисование квадрата.
    '''
    Отрисовка кругов.
    '''
    def file_save(self):  # Функция сохранения файла png.
        self.file_name = self.e.get()
        # Получение имени файла.
        ImageGrab.grab((self.canvas.winfo_rootx(), self.canvas.winfo_rooty(), self.canvas.winfo_width(),
                        self.canvas.winfo_height())).save(self.file_name + '.png')
        # Запечатление и сохранение рисунка в папке приложения.
    '''
    Сохранение файлов
    '''

    def set_ui(self):
        self.parent.title("Симметричное рисование")  # Имя окна
        self.pack(fill=BOTH, expand=1)  # Размещение элементов на родительском окне
        self.columnconfigure(8, weight=1)
        self.rowconfigure(2, weight=1)  # Количество столбцов и строк
        for i in range(9):
            self.grid_columnconfigure(i, minsize=145)  # Минимальная ширина столбца
        self.canvas = Canvas(self, bg=self.color_canvas)
        self.scale_red = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_brush = Scale(self, from_=1, to=20, orient=HORIZONTAL)
        self.e = Entry(self)
        self.scale_symmetry = Scale(self, from_=1, to=10, orient=HORIZONTAL)
        self.scale_green = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        self.scale_blue = Scale(self, from_=0, to=255, orient=HORIZONTAL)
        # Задаем canvas и шкалы, значения которых необходимо получать в вызываемых функциях.
        self.canvas.grid(row=2, column=0, columnspan=9, sticky=E + W + S + N)
        # Расположение canvas, его размер в столбцах и возможность растягивания.
        self.canvas.bind("<B1-Motion>", self.draw)  # Отслеживание за счет движения + нажатия левой кнопки мыши
        canvas_color_setting_btn = Button(self, text="Set canvas color",
                                          width=16, command=lambda: self.set_color_canvas())
        canvas_color_setting_btn.grid(row=1, column=7)
        # Кнопка для задания цвета canvas.
        self.scale_red.grid(row=0, column=1)
        label_red = Label(self, text='Red')
        label_red.grid(row=0, column=0)
        # Расположение шкалы красного и ее названия.
        self.scale_green.grid(row=0, column=3)
        label_green = Label(self, text='Green')
        label_green.grid(row=0, column=2)
        # Расположение шкалы зеленого и ее названия.
        self.scale_blue.grid(row=0, column=5)
        label_blue = Label(self, text='Blue')
        label_blue.grid(row=0, column=4)
        # Расположение шкалы голубого и ее названия.
        symmetry_lab = Label(self, text="Symmetry number")
        symmetry_lab.grid(row=1, column=0, padx=6)
        self.scale_symmetry.grid(row=1, column=1)
        # Расположение шкалы симметрий и ее названия.
        clean_btn = Button(self, text="Clean", width=16, command=lambda: self.canvas.delete('all'))
        clean_btn.grid(row=1, column=8)
        # Кнопка для полной очистки экрана.
        Label(self, text="File name").grid(row=1, column=2)
        self.e.grid(row=1, column=3)
        self.e.insert(10, "Untitled")
        # Расположение названия и окна для ввода имени файла.
        file_btn = Button(self, text="Save", width=16, command=lambda: self.file_save())
        file_btn.grid(row=1, column=4)
        # Расположение кнопки для сохранения файла.
        circle_btn = Button(self, text="Draw circles", width=16, command=lambda: self.set_type('circle'))
        circle_btn.grid(row=0, column=6)
        # Расположение кнопки, задающей тип фигуры круг.
        triangle_btn = Button(self, text="Draw triangles", width=16, command=lambda: self.set_type('triangle'))
        triangle_btn.grid(row=0, column=7)
        # Расположение кнопки, задающей тип фигуры треугольник.
        rectangle_btn = Button(self, text="Draw rectangles", width=16, command=lambda: self.set_type('rectangle'))
        rectangle_btn.grid(row=0, column=8)
        # Расположение кнопки, задающей тип фигуры квадрат.
        self.scale_brush.grid(row=1, column=5)
        label_brush = Label(self, text='Brush size')
        label_brush.grid(row=1, column=6)
                # Расположение шкалы размера кисти и ее названия.
        '''
        Определение виджетов и их месторасположения
        '''

    def set_type(self, n):
        if n == 'circle':
            self.type = 'triangle'
        if n == 'rectangle':
            self.type = 'rectangle'
        if n == 'triangle':
            self.type = 'triangle'
    '''
    Задание типа фигуры
    '''

if __name__ == '__main__':
    root = Tk()
    root.geometry(str(int(root.winfo_screenwidth()))+'x'+str(int(root.winfo_screenheight())))
    app = Paint(root)
    root.mainloop()
# Вызов окна.

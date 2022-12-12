import tkinter as tk
from matplotlib.mathtext import math_to_image
from io import BytesIO
from PIL import ImageTk, Image
from Scrolling import ScrollableImage


class Application(tk.Frame):
    def __init__(self, f, f2, master=None):
        self.master = master
        tk.Frame.__init__(self, master)
        self.pack()
        self.fin = f
        self.fin2 = f2
        self.createWidgets()



    def createWidgets(self):

        #Создаём буферную переменную для хранения будущей картинки
        buffer = BytesIO()

        #Преобразуем наш latex-код в картинку с раширением .png и засовываем её в буфер
        math_to_image(self.fin, buffer, dpi=250, format='png')

        #Ставим "курсор" на начало буфера
        buffer.seek(0)

        # Открываем нашу картинку с помощью библеотеки PIL
        pimage= Image.open(buffer)

        #Создаём картинку для tkinter'а
        image = ImageTk.PhotoImage(pimage)

        #Создаём перменную типа ScrollableImage с помещённой в него формулой
        image_window = ScrollableImage(self.master, image=image, scrollbarwidth=9,
                                       width=900, height=100)

        #Упаковывааем
        image_window.pack()

        #Делаем всё тоже самое, но для второй формулы
        buffer2 = BytesIO()
        math_to_image(self.fin2, buffer2, dpi=250, format='png')

        buffer2.seek(0)
        pimage = Image.open(buffer2)

        image = ImageTk.PhotoImage(pimage)

        image_window = ScrollableImage(self.master, image=image, scrollbarwidth=9,
                                       width=900, height=100)
        image_window.pack()



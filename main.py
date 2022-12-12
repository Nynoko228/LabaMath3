import matplotlib.pyplot as plt  # для графиков
import math
from threading import Thread
from Form import Application

import tkinter as tk  # для интерфейса
from tkinter import ttk


# Функция formula() составляет latex-код наших формул
def formula():
    form1 = "Формулы для 3-их разностей: " \
            "Правые: " + r"$\frac{1}{2h}(-y_{2}+4y_{1}-3y_{0})$ " \
                         "Центральные: " + r"$\frac{1}{2h}(y_{1}-y_{-1})$ " \
                                           "Левые: " + r"$\frac{1}{2h}(3y_{0}-4y_{-1}+y_{-2})$ "
    form2 = "Формулы для 5-ых разностей: " \
            "Правые: " + r"$\frac{1}{12h}(-3y_{4}+16y_{3}-36y_{2}+48y_{1}-25y_{0})$ " \
                         "Центральные: " + r"$\frac{1}{12h}(-y_{2}+8y_{1}-8y_{-1}+y_{-2})$ " \
                                           "Левые: " + r"$\frac{1}{12h}(3y_{-4}-16y_{-3}+36y_{-2}-48y_{-1}+25y_{0})$"
    root = tk.Toplevel()
    app = Application(form1, form2, master=root)
    app.mainloop()

# Функция mainWidget() создаёт виджет с таблицей
def mainWidget():
    root1 = tk.Tk()
    root1.geometry("700x500")
    game_frame = tk.Frame(root1)
    game_frame.pack()

    # скроллбар
    game_scroll = tk.Scrollbar(game_frame, orient='vertical')
    game_scroll.pack(side="right", fill="y")
    my_game = ttk.Treeview(game_frame, yscrollcommand=game_scroll.set, height=15)

    my_game.pack()

    game_scroll.config(command=my_game.yview)

    my_game['columns'] = ('ugol', 'sin', 'cos', '3', '5')

    # Форматируем колонки
    my_game.column("#0", width=0, stretch='no')
    my_game.column("ugol", anchor='center', width=50)
    my_game.column("sin", anchor='center', width=120)
    my_game.column("cos", anchor='center', width=140)
    my_game.column("3", anchor='center', width=140)
    my_game.column("5", anchor='center', width=145)

    # Создаём имена для колонок
    my_game.heading("#0", text="", anchor='center')
    my_game.heading("ugol", text="Угол(град)", anchor='center')
    my_game.heading("sin", text="Sin(угла)", anchor='center')
    my_game.heading("cos", text="Cos(угла)", anchor='center')
    my_game.heading("3", text="Производная по 3-им\nразностям", anchor='center')
    my_game.heading("5", text="Производная по 5-ым\nразностям", anchor='center')

    # Заполняем таблицу данными
    for i in range(46):
        my_game.insert(parent='', index='end', iid=i, text='',
                       values=(xL[i], yL[i], cosX[i], y3[i], y5[i]))
    my_game.pack()

    root1.mainloop()


# Функция Math() просто считает производные
def Math():
    global h, y3, y5, xL, yL, cosX
    for i in range(46):
        xL.append(i * 2)
        yL.append(math.sin(math.radians(i * 2)))
        cosX.append(math.cos(math.radians(i * 2)))
    print(xL, yL, cosX, sep="\n")
    y3.append(math.degrees((1 / (2 * h)) * (-3 * yL[0] + 4 * yL[1] - yL[2])))
    for i in range(1, 45):
        y3.append(math.degrees((1 / (2 * h)) * (yL[i + 1] - yL[i - 1])))
    y3.append(math.degrees((1 / (2 * h)) * ((yL[-3]) - 4 * (yL[-2]) + 3 * (yL[-1]))))
    print("Производная по 3-им разностям: ", y3)

    y5.append(math.degrees((1 / (12 * h)) * (-25 * yL[0] + 48 * yL[1] - 36 * yL[2] + 16 * yL[3] - 3 * yL[4])))
    y5.append(math.degrees((1 / (12 * h)) * (-25 * yL[1] + 48 * yL[2] - 36 * yL[3] + 16 * yL[4] - 3 * yL[5])))
    for i in range(2, 44):
        y5.append(math.degrees((1 / (12 * h)) * (yL[i - 2] - 8 * yL[i - 1] + 8 * yL[i + 1] - yL[i + 2])))
    y5.append(math.degrees((1 / (12 * h)) * (25 * yL[-2] - 48 * yL[-3] + 36 * yL[-4] - 16 * yL[-5] + 3 * yL[-6])))
    y5.append(math.degrees((1 / (12 * h)) * (25 * yL[-1] - 48 * yL[-2] + 36 * yL[-3] - 16 * yL[-4] + 3 * yL[-5])))
    print("Производная по 5-ым разностям: ", y5)
    thread1 = Thread(target=mainWidget)
    thread2 = Thread(target=draw)
    thread3 = Thread(target=formula)

    thread1.start()
    thread2.start()
    thread3.start()


# Функция draw рисует наши кривые на координатной плоскости
def draw():
    global xL, yL, y3, y5, cosX
    print(len(xL), len(yL), len(cosX), len(y3), len(y5))
    plt.plot(xL, y3, label="График по 3-им разностям")
    plt.plot(xL, y5, label="График по 5-ым разностям")
    plt.plot(xL, yL, label="График sin(x)")
    plt.plot(xL, cosX, label="График cos(x)")
    plt.legend(loc="upper right")
    plt.show()


h = 2
y3, y5, xL, yL, cosX = [], [], [], [], []
Math()

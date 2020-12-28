from tkinter import *

# zmienne wielkości okna
x = 20
y = 20
length = y * 30
width = x * 30

# ustawienia root
root = Tk()
root.title("Gra w życie")
root.iconbitmap("icon.ico")
resolution = str(width) + 'x' + str(length + 86)
root.geometry(resolution)

# ustawienia canvas
canvas = Canvas(root, width=1000, height=1000)
canvas.place(x=0, y=30)

def draw():
"""rysuje planszę"""
    for x_1 in range(x):
        for y_1 in range(y):
            canvas.create_rectangle(30 * x_1, 30 * y_1, 20 + 30 * x_1, 20 + 30 * y_1, fill='red')

def start():
"""rozpoczyna symulacje"""
    draw()
    button_start.place_forget()
    button_stop.place(x=0, y=length + 55)

def stop():
    button_stop.place_forget()
    button_start.place(x=0, y=length + 55)

def next(a):
    if a == 1:
        draw()
    # else:
    #     for i in range(a):
    #         rysuj()

# utworzone przyciski
button_reset = Button(root, text="Przywróć do stanu początkowego")
button_clear = Button(root, text="Wyczyść")

button_next = Button(root, text="Jeden ruch", command=lambda: next(1))
button_next_5 = Button(root, text="5 ruchów", command=lambda: next(5))
button_next_10 = Button(root, text="10 ruchów", command=lambda: next(10))

button_start = Button(root, text="Rozpocznij", command=start)
button_stop = Button(root, text="Wstrzymaj", command=stop)

# wypisanie przycisków do okna
button_reset.place(x=0, y=0)
button_clear.place(x=189, y=0)

button_next.place(x=0, y=length + 25)
button_next_5.place(x=69, y=length + 25)
button_next_10.place(x=130, y=length + 25)
button_start.place(x=0, y=length + 55)

root.mainloop()
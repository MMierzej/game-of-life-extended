from tkinter import *

# ustawienia root
root = Tk()
root.title("Gra w życie")
root.iconbitmap("icon.ico")

# testowa mapa
mapa = [['_' for _ in range(10)] for _ in range(10)]


# Rysuje planszę
def rysuj():
    for x in range(10):
        for y in range(10):
            label = Label(root, text=mapa[x][y])
            label.grid(row=x, column=y + 3)


# Podmienia Rozpocznij na Wstrzymaj | Wstrzymaj na Rozpocznij / Rozpoczęcie automatycznego aktualizowania się mapy
def start():
    rysuj()
    button_start.grid_forget()
    button_stop.grid(row=2, column=0)


def stop():
    button_stop.grid_forget()
    button_start.grid(row=2, column=0)


def next(a):
    if a == 1:
        rysuj()
    # else:
    #     for i in range(a):
    #         rysuj()


# Utworzone przyciski
button_reset = Button(root, text="Przywróć do stanu początkowego")
button_clear = Button(root, text="Wyczyść")

button_next = Button(root, text="Jeden ruch", command=lambda: next(1))
button_next_5 = Button(root, text="5 ruchów", command=lambda: next(5))
button_next_10 = Button(root, text="10 ruchów", command=lambda: next(10))

button_start = Button(root, text="Rozpocznij", command=start)
button_stop = Button(root, text="Wstrzymaj", command=stop)
# Wypisanie przycisków
button_reset.grid(row=0, column=0, columnspan=2)
button_clear.grid(row=0, column=2)

button_next.grid(row=1, column=0)
button_next_5.grid(row=1, column=1)
button_next_10.grid(row=1, column=2)

button_start.grid(row=2, column=0)

# Rysowanie mapki


root.mainloop()

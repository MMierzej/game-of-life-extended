from tkinter import *
from logic import *

# zmienne wielkości okna
x = 10
y = 10
length = y * 30
width = x * 30

# Tablica testowa
board = generate()

# ustawienia root
root = Tk()
root.title("Gra w życie")
root.iconbitmap("icon.ico")
resolution = str(width + 275) + 'x' + str(length + 20)
root.geometry(resolution)
root.resizable(False, False)

# ustawienia canvas
frame_board = Canvas(root, width=1000, height=1000)
frame_board.place(x=260, y=0)
frame_board.create_rectangle(5, 5, length + 10, width + 10)

board_gui = Canvas(root, width=width - 5, height=length - 5)
board_gui.place(x=270, y=10)

frame = Canvas(root, width=255, height=505)
frame.place(x=0, y=0)
frame.create_rectangle(5, 5, 255, 505)


def clicked_left(event):
    x_click = event.x // 30
    y_click = event.y // 30
    if board[x_click][y_click][0] < 3:
        board[x_click][y_click][0] += 1
        if board[x_click][y_click][0] == 3:
            board[x_click][y_click][1] = LIFE_3
            board_gui.create_rectangle(30 * x_click + 3, 30 * y_click + 3, 20 + 30 * x_click + 3, 20 + 30 * y_click + 3,
                                       fill='#1B1B1B',
                                       tags=f'{x_click},{y_click}')
        elif board[x_click][y_click][0] == 2:
            board[x_click][y_click][1] = LIFE_2
            board_gui.create_rectangle(30 * x_click + 3, 30 * y_click + 3, 20 + 30 * x_click + 3, 20 + 30 * y_click + 3,
                                       fill='#525151',
                                       tags=f'{x_click},{y_click}')
        elif board[x_click][y_click][0] == 1:
            board[x_click][y_click][1] = LIFE_1
            board_gui.create_rectangle(30 * x_click + 3, 30 * y_click + 3, 20 + 30 * x_click + 3, 20 + 30 * y_click + 3,
                                       fill='#949494',
                                       tags=f'{x_click},{y_click}')


def clicked_right(event):
    x_click = event.x // 30
    y_click = event.y // 30
    if board[x_click][y_click][0] != 0:
        board[x_click][y_click][0] -= 1
        if board[x_click][y_click][0] == 0:
            board[x_click][y_click][1] = 0
            board_gui.create_rectangle(30 * x_click + 3, 30 * y_click + 3, 20 + 30 * x_click + 3, 20 + 30 * y_click + 3,
                                       fill='white',
                                       tags=f'{x_click},{y_click}')
        elif board[x_click][y_click][0] == 1:
            board[x_click][y_click][1] = LIFE_1
            board_gui.create_rectangle(30 * x_click + 3, 30 * y_click + 3, 20 + 30 * x_click + 3, 20 + 30 * y_click + 3,
                                       fill='#949494',
                                       tags=f'{x_click},{y_click}')
        elif board[x_click][y_click][0] == 2:
            board[x_click][y_click][1] = LIFE_2
            board_gui.create_rectangle(30 * x_click + 3, 30 * y_click + 3, 20 + 30 * x_click + 3, 20 + 30 * y_click + 3,
                                       fill='#525151',
                                       tags=f'{x_click},{y_click}')


def draw_board():
    """rysuje planszę"""
    for x_1 in range(x):
        for y_1 in range(y):
            if board[x_1][y_1][0] == 3:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#000000',
                                           tags=f'{x_1},{y_1}')
            elif board[x_1][y_1][0] == 2:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#525151',
                                           tags=f'{x_1},{y_1}')
            elif board[x_1][y_1][0] == 1:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#949494',
                                           tags=f'{x_1},{y_1}')
            else:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='white',
                                           tags=f'{x_1},{y_1}')
            board_gui.tag_bind(f'{x_1},{y_1}', '<Button-1>', clicked_left)
            board_gui.tag_bind(f'{x_1},{y_1}', '<Button-3>', clicked_right)


def clear():
    for x_1 in range(x):
        for y_1 in range(y):
            board[x_1][y_1][0] = 0
            board[x_1][y_1][1] = 0
            board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                       fill='white',
                                       tags=f'{x_1},{y_1}')
            board_gui.tag_bind(f'{x_1},{y_1}', '<Button-1>', clicked_left)
            board_gui.tag_bind(f'{x_1},{y_1}', '<Button-3>', clicked_right)


def new_board():
    global board
    board = generate()
    draw_board()


def start():
    """rozpoczyna symulacje"""
    button_start.place_forget()
    button_stop.place(x=7, y=123)


def stop():
    button_stop.place_forget()
    button_start.place(x=7, y=123)


def step(a):
    global REFRESH_IT
    REFRESH_IT = a
    print(REFRESH_IT)


# utworzone przyciski
button_reset = Button(root, text="Generuj nową planszę", command=new_board)
button_clear = Button(root, text="Wyczyść", command=clear)

button_next = Button(root, text="Jeden ruch", command=lambda: step(1))
button_next_5 = Button(root, text="5 ruchów", command=lambda: step(5))
button_next_10 = Button(root, text="10 ruchów", command=lambda: step(10))

button_start = Button(root, text="Rozpocznij", command=start)
button_stop = Button(root, text="Wstrzymaj", command=stop)

# wypisanie przycisków do okna
button_reset.place(x=7, y=7)
button_clear.place(x=197, y=7)

button_next.place(x=7, y=65)
button_next_5.place(x=76, y=65)
button_next_10.place(x=137, y=65)
button_start.place(x=7, y=123)

root.mainloop()

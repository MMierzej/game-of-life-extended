from tkinter import *
from logic import *

# zmienne wielkości okna
x = 10
y = 10
length = y * 30
width = x * 30
counter = 0
board = [[[0, 0] for i in range(x)] for j in range(y)]
prev = cp.deepcopy(board)
board_d = {}
neighbours_d = {}
run = True

# ustawienia root
root = Tk()
root.title("Gra w życie")
# root.iconbitmap("icon.ico")
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
    
    board[x_click][y_click][0] += 1
    if board[x_click][y_click][0] == 4:
        board[x_click][y_click][0] = 0
    
    draw_board()

def clicked_right(event):
    x_click = event.x // 30
    y_click = event.y // 30

    board[x_click][y_click][0] -= 1
    if board[x_click][y_click][0] == -1:
        board[x_click][y_click][0] = 3
    
    draw_board()

def draw_board():
    """rysuje planszę"""

    for x_1 in range(x):
        for y_1 in range(y):
            if board[x_1][y_1][0] == 3:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#ef7c27',
                                           tags=f'{x_1},{y_1}')
            elif board[x_1][y_1][0] == 2:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#009C11',
                                           tags=f'{x_1},{y_1}')
            elif board[x_1][y_1][0] == 1:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#43b0bd',
                                           tags=f'{x_1},{y_1}')
            else:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#e3e3e3',
                                           tags=f'{x_1},{y_1}')
            board_gui.tag_bind(f'{x_1},{y_1}', '<Button-1>', clicked_left)
            board_gui.tag_bind(f'{x_1},{y_1}', '<Button-3>', clicked_right)
    
    board_gui.update()


def clear():
    for x_1 in range(x):
        for y_1 in range(y):
            board[x_1][y_1][0] = 0
            board[x_1][y_1][1] = 0

    draw_board()

def new_board():
    global board
    global prev

    global board_d
    global neighbours_d

    global counter

    board = generate(x, y)
    prev = cp.deepcopy(board)

    board_d = dd(lambda: 0)
    neighbours_d = dd(lambda: 0)

    counter = 0

    draw_board()

def start():
    """rozpoczyna symulacje"""
    button_start.place_forget()
    button_stop.place(x=7, y=123)

    global run
    run = True

    while run:
        step(1)

def stop():
    global run
    run = False

    button_stop.place_forget()
    button_start.place(x=7, y=123)

def step(a):
    global counter

    for _ in range(a):
        clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
        next_state(board, prev, neighbours_d, counter)  # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1
        draw_board()
        time.sleep(0.1)

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


new_board()
clear()

root.mainloop()

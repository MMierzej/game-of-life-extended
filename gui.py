#!/usr/bin/env python3
from tkinter import *
from logic import *
import time
import platform


LIFE = [1, 1, 1]
NB = [3, 3, 3]
SPAWN = [1, 1, 1]
QUAKE = 2
MUT = 0
TEMPO = 7


# zmienne wielkości okna
x = 20
y = 20
height = y * 30
width = x * 30
fwidth = max(width + 300, 900)
fheight = height + 350

# setup zmiennych
counter = 0
board = [[[0, 0] for i in range(x)] for j in range(y)]
prev = cp.deepcopy(board)
neighbours_d = dd(lambda : 0)
run = False


# ustawienia root
root = Tk()
root.title("Gra w życie")

if "Linux" not in platform.platform():
    root.iconbitmap("icon.ico")

resolution = str(fwidth) + 'x' + str(fheight)
root.geometry(resolution)
root.resizable(False, False)


# ustawienia canvas
board_canvas = Canvas(root, width=width + 10, height=height + 10)
board_canvas.place(x=fwidth // 2 - width // 2 - 10, y=60)
board_canvas.create_rectangle(5, 5, width + 10, height + 10)

board_gui = Canvas(root, width=width - 5, height=height - 5)
board_gui.place(x=fwidth // 2 - width // 2, y=70)

upper_canvas = Canvas(root, width=fwidth - 10, height=40)
upper_canvas.place(x=0, y=10)
upper_canvas.create_rectangle(fwidth // 2 - 180, 5, fwidth // 2 + 177, 40)


def clicked_left(event):
    x_click = event.x // 30
    y_click = event.y // 30

    board[y_click][x_click][0] = (board[y_click][x_click][0] + 1) % 4
    board[y_click][x_click][1] = LIFE[board[y_click][x_click][0] - 1]

    if is_empty(board):
        button_next['state'] = DISABLED
        button_next_5['state'] = DISABLED
        button_next_10['state'] = DISABLED
    else:
        button_next['state'] = NORMAL
        button_next_5['state'] = NORMAL
        button_next_10['state'] = NORMAL
        
    draw_board()


def clicked_right(event):
    x_click = event.x // 30
    y_click = event.y // 30

    board[y_click][x_click][1] -= 1

    if board[y_click][x_click][1] <= 0:
        board[y_click][x_click][0] = 0
        board[y_click][x_click][1] = 0

    if is_empty(board):
        button_next['state'] = DISABLED
        button_next_5['state'] = DISABLED
        button_next_10['state'] = DISABLED

    draw_board()


def draw_board():
    """rysuje planszę"""
    board_gui.delete('all')
    
    s1, s2, s3 = count(board)
    s1_label['text'] = f': {s1}'
    s2_label['text'] = f': {s2}'
    s3_label['text'] = f': {s3}'
    gen_label['text'] = f'Czas: {counter}'


    for y_1 in range(y):
        for x_1 in range(x):

            if board[y_1][x_1][0] == 1:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#f1c40f',  # żółty
                                           tags=f'{y_1},{x_1}')

            elif board[y_1][x_1][0] == 2:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#cb4335',  # czerwony
                                           tags=f'{y_1},{x_1}')

            elif board[y_1][x_1][0] == 3:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#2980b9',  # niebieski
                                           tags=f'{y_1},{x_1}')

            else:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#e3e3e3',
                                           tags=f'{y_1},{x_1}')

            board_gui.tag_bind(f'{y_1},{x_1}', '<Button-1>', clicked_left)
            board_gui.tag_bind(f'{y_1},{x_1}', '<Button-3>', clicked_right)
    
    board_gui.update()


def is_empty(board):
    for i in range(y):
        for k in range(x):
            if board[i][k][0] != 0:
                return False
    
    return True


def clear():
    global neighbours_d
    global counter
    global run

    if run:
        start_stop()

    for x_1 in range(x):
        for y_1 in range(y):
            board[y_1][x_1][0] = 0
            board[y_1][x_1][1] = 0
    
    neighbours_d = dd(lambda: 0)
    counter = 0

    draw_board()


def new_board():
    global board
    global prev
    global neighbours_d
    global counter

    board = generate(x, y, LIFE, SPAWN)
    prev = cp.deepcopy(board)
    neighbours_d = dd(lambda: 0)
    counter = 0

    draw_board()


def clear_all():
    clear()

    button_next['state'] = DISABLED
    button_next_5['state'] = DISABLED
    button_next_10['state'] = DISABLED


def gen_board():
    new_board()

    button_next['state'] = NORMAL
    button_next_5['state'] = NORMAL
    button_next_10['state'] = NORMAL


def start_stop():
    global run

    if button_start['text'] == 'Rozpocznij':
        button_next['state'] = DISABLED
        button_next_5['state'] = DISABLED
        button_next_10['state'] = DISABLED
        button_start['text'] = 'Wstrzymaj'

        if is_empty(board):
            new_board()

        run = True
        while run:
            step(1)
    
    elif button_start['text'] == 'Wstrzymaj':
        if not is_empty(board):
            button_next['state'] = NORMAL
            button_next_5['state'] = NORMAL
            button_next_10['state'] = NORMAL

        button_start['text'] = 'Rozpocznij'
        run = False


def step(a):
    global counter

    button_generate['state'] = DISABLED

    i = 0
    while i < a:
        clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
        next_state(board, prev, neighbours_d, counter, LIFE, NB, SPAWN, QUAKE, MUT)  # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1
        i += 1
        draw_board()
        time.sleep(1 - (TEMPO - 1) / 10)
    
    button_generate['state'] = NORMAL


def set_life(value, index):
    LIFE[index] = int(value)

def set_nb(value, index):
    NB[index] = int(value)

def set_tempo(val):
    global TEMPO
    TEMPO = int(val)

def set_sub_it(val):
    global QUAKE
    QUAKE = int(val)

def set_rand_it(val):
    global MUT
    MUT = int(val)

def set_spawn(val, index):
    global SPAWN
    SPAWN[index] = int(val)


controls_canvas = Canvas(root, width = fwidth - 10, height=300)
controls_canvas.place(x=5, y=70 + height + 10)
controls_canvas.create_rectangle(5, 5, fwidth - 15, 260)


# scoreboard
canvas_scoreboard = Canvas(root, width=140, height=height + 10)
canvas_scoreboard.place(x=0, y=60)
canvas_scoreboard.create_rectangle(40, height // 2 - 55, 60, height // 2 - 35, fill='#f1c40f')
canvas_scoreboard.create_rectangle(40, height // 2 - 5, 60, height // 2 + 15, fill='#cb4335')
canvas_scoreboard.create_rectangle(40, height // 2 + 45, 60, height // 2 + 65, fill='#2980b9')

s1_label = Label(canvas_scoreboard, text='', font=('courier new', 13))
s2_label = Label(canvas_scoreboard, text='', font=('courier new', 13))
s3_label = Label(canvas_scoreboard, text='', font=('courier new', 13))
s1_label.place(x=61, y=height // 2 - 55)
s2_label.place(x=61, y=height // 2 - 5)
s3_label.place(x=61, y=height // 2 + 45)

gen_label = Label(root, text='', font=('courier new', 14))
gen_label.place(x=fwidth // 2 + width // 2 + 20, y=55 + height // 2)


# przyciski kontrolujące przebieg symulacji
button_generate = Button(upper_canvas, width=10, text="Generuj", command=gen_board)
button_clear = Button(upper_canvas, width=10, text="Wyczyść", command=clear_all)
button_start = Button(upper_canvas, width=10, text="Rozpocznij", command=start_stop)
button_generate.place(x=fwidth // 2 - 55, y=7)
button_start.place(x=fwidth // 2 - 175, y=7)
button_clear.place(x=fwidth // 2 + 65, y=7)

button_next = Button(controls_canvas, width=10, text="1 ruch", command=lambda: step(1), state='disable')
button_next_5 = Button(controls_canvas, width=10, text="5 ruchów", command=lambda: step(5), state='disable')
button_next_10 = Button(controls_canvas, width=10, text="10 ruchów", command=lambda: step(10), state='disable')
button_next.place(x=fwidth // 2 - 175, y=15)
button_next_5.place(x=fwidth // 2 - 55, y=15)
button_next_10.place(x=fwidth // 2 + 65, y=15)


# maks. punkty życia
label_life = Label(controls_canvas, text='Punkty życia:', font=('courier new', 13))
label_life.place(x=27 + (fwidth - 700) // 2, y=67)

controls_canvas.create_rectangle(21 + (fwidth - 700) // 2, 115, 41 + (fwidth - 700) // 2, 135, fill='#f1c40f')
controls_canvas.create_rectangle(21 + (fwidth - 700) // 2, 165, 41 + (fwidth - 700) // 2, 185, fill='#cb4335')
controls_canvas.create_rectangle(21 + (fwidth - 700) // 2, 215, 41 + (fwidth - 700) // 2, 235, fill='#2980b9')

sl_life_1 = Scale(controls_canvas, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_life(x, 0))
sl_life_1.set(LIFE[0])
sl_life_1.place(x=60 + (fwidth - 700) // 2, y=95)

sl_life_2 = Scale(controls_canvas, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_life(x, 1))
sl_life_2.set(LIFE[1])
sl_life_2.place(x=60 + (fwidth - 700) // 2, y=145)

sl_life_3 = Scale(controls_canvas, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_life(x, 2))
sl_life_3.set(LIFE[2])
sl_life_3.place(x=60 + (fwidth - 700) // 2, y=195)


# liczba sąsiadów do pojawienia się
label_nb = Label(controls_canvas, text='Sąsiedzi:', font=('courier new', 13))
label_nb.place(x=195 + (fwidth - 700) // 2, y=67)

sl_nb_1 = Scale(controls_canvas, orient=HORIZONTAL, from_=1, to=8, command=lambda x : set_nb(x, 0))
sl_nb_1.set(NB[0])
sl_nb_1.place(x=190 + (fwidth - 700) // 2, y=95)

sl_nb_2 = Scale(controls_canvas, orient=HORIZONTAL, from_=1, to=8, command=lambda x : set_nb(x, 1))
sl_nb_2.set(NB[1])
sl_nb_2.place(x=190 + (fwidth - 700) // 2, y=145)

sl_nb_3 = Scale(controls_canvas, orient=HORIZONTAL, from_=1, to=8, command=lambda x : set_nb(x, 2))
sl_nb_3.set(NB[2])
sl_nb_3.place(x=190 + (fwidth - 700) // 2, y=195)


# czestotliwosc pojawiania sie
label_sf = Label(controls_canvas, text='Reprodukcja:', font=('courier new', 13))
label_sf.place(x=310 + (fwidth - 700) // 2, y=67)

sl_sf_1 = Scale(controls_canvas, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_spawn(x, 0))
sl_sf_1.set(SPAWN[0])
sl_sf_1.place(x=320 + (fwidth - 700) // 2, y=95)

sl_sf_2 = Scale(controls_canvas, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_spawn(x, 1))
sl_sf_2.set(SPAWN[1])
sl_sf_2.place(x=320 + (fwidth - 700) // 2, y=145)

sl_sf_3 = Scale(controls_canvas, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_spawn(x, 2))
sl_sf_3.set(SPAWN[2])
sl_sf_3.place(x=320 + (fwidth - 700) // 2, y=195)


# globalne zmienne dotyczace rozgrywki
label_ctrl = Label(controls_canvas, text='Rozgrywka:', font=('courier new', 13))
label_ctrl.place(x=530 + (fwidth - 700) // 2, y=67)

label_tempo = Label(controls_canvas, text='Tempo:', font=('courier new', 13))
label_tempo.place(x=485 + (fwidth - 700) // 2, y=114)
sl_tempo = Scale(controls_canvas, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_tempo(x))
sl_tempo.set(TEMPO)
sl_tempo.place(x=560 + (fwidth - 700) // 2, y=95)

label_mut = Label(controls_canvas, text='Mutacje:', font=('courier new', 13))
label_mut.place(x=465 + (fwidth - 700) // 2, y=214)
sl_mut = Scale(controls_canvas, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_rand_it(x))
sl_mut.set(MUT)
sl_mut.place(x=560 + (fwidth - 700) // 2, y=195)

label_eq = Label(controls_canvas, text='Quake:', font=('courier new', 13))
label_eq.place(x=485 + (fwidth - 700) // 2, y=164)
sl_eq = Scale(controls_canvas, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_sub_it(x))
sl_eq.set(QUAKE)
sl_eq.place(x=560 + (fwidth - 700) // 2, y=145)


clear_all()

root.mainloop()

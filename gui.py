#!/usr/bin/env python3
from tkinter import *
from typing import runtime_checkable
from logic import *
import platform


LIFE = [1, 1, 1]
NB = [3, 3, 3]
SPAWN = [1, 1, 1]
QUAKE = 2
MUT = 0
TEMPO = 8

# zmienne wielkości okna
x = 12
y = 12
height = y * 30
width = x * 30
fwidth = width + 100 if width > 600 else 700
fheight = height + 350

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
root.minsize(400, 400)
root.geometry(resolution)
root.resizable(False, False)

# ustawienia canvas
frame_board = Canvas(root, width=width + 10, height=height + 10)
frame_board.place(x=fwidth // 2 - width // 2 - 10, y=60)
frame_board.create_rectangle(5, 5, width + 10, height + 10)

board_gui = Canvas(root, width=width - 5, height=height - 5)
board_gui.place(x=fwidth // 2 - width // 2, y=70)

frame = Canvas(root, width=fwidth - 10, height=40)
frame.place(x=5, y=10)
frame.create_rectangle(fwidth // 2 - 180, 5, fwidth // 2 + 177, 40)

frame_controls = Canvas(root, width = fwidth - 10, height=300)
frame_controls.place(x=5, y=70 + height + 10)
frame_controls.create_rectangle(5, 5, fwidth - 15, 260)


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
    s1_lab['text'] = f': {s1}'
    s2_lab['text'] = f': {s2}'
    s3_lab['text'] = f': {s3}'
    gen_lab['text'] = f'Czas: {counter}'


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

        if is_empty(board):
            new_board()

        button_start['text'] = 'Wstrzymaj'
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
    i = 0

    button_generate['state'] = 'disable'

    while i < a:
        clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
        next_state(board, prev, neighbours_d, counter, LIFE, NB, SPAWN, QUAKE, MUT)  # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1
        draw_board()
        time.sleep(1 - (TEMPO - 1) / 10)
        i += 1
    
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


# scoreboard
canvas_scoreboard = Canvas(root, width=150, height=height + 10)
canvas_scoreboard.place(x=5, y=60)
canvas_scoreboard.create_rectangle(40, height // 2 - 55, 60, height // 2 - 35, fill='#f1c40f')
canvas_scoreboard.create_rectangle(40, height // 2 - 5, 60, height // 2 + 15, fill='#cb4335')
canvas_scoreboard.create_rectangle(40, height // 2 + 45, 60, height // 2 + 65, fill='#2980b9')
s1_lab = Label(canvas_scoreboard, text='', font=('courier new', 13))
s2_lab = Label(canvas_scoreboard, text='', font=('courier new', 13))
s3_lab = Label(canvas_scoreboard, text='', font=('courier new', 13))
s1_lab.place(x=61, y=height // 2 - 55)
s2_lab.place(x=61, y=height // 2 - 5)
s3_lab.place(x=61, y=height // 2 + 45)
gen_lab = Label(root, text='', font=('courier new', 14))
gen_lab.place(x=fwidth // 2 + width // 2 + 20, y=55 + height // 2)

# utworzone przyciski
button_generate = Button(frame, width=10, text="Generuj", command=gen_board)
button_clear = Button(frame, width=10, text="Wyczyść", command=clear_all)
button_start = Button(frame, width=10, text="Rozpocznij", command=start_stop)

button_next = Button(frame_controls, width=10, text="1 ruch", command=lambda: step(1), state='disable')
button_next_5 = Button(frame_controls, width=10, text="5 ruchów", command=lambda: step(5), state='disable')
button_next_10 = Button(frame_controls, width=10, text="10 ruchów", command=lambda: step(10), state='disable')

# wypisanie przycisków do okna
button_generate.place(x=fwidth // 2 - 55, y=7)
button_start.place(x=fwidth // 2 - 175, y=7)
button_clear.place(x=fwidth // 2 + 65, y=7)

button_next.place(x=fwidth // 2 - 175, y=15)
button_next_5.place(x=fwidth // 2 - 55, y=15)
button_next_10.place(x=fwidth // 2 + 65, y=15)

sl_life_1 = Scale(frame_controls, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_life(x, 0))
sl_life_1.set(LIFE[0])
sl_life_1.place(x=60, y=95)

sl_life_2 = Scale(frame_controls, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_life(x, 1))
sl_life_2.set(LIFE[1])
sl_life_2.place(x=60, y=145)

sl_life_3 = Scale(frame_controls, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_life(x, 2))
sl_life_3.set(LIFE[2])
sl_life_3.place(x=60, y=195)

frame_controls.create_rectangle(21, 116, 41, 136, fill='#f1c40f')
frame_controls.create_rectangle(21, 166, 41, 186, fill='#cb4335')
frame_controls.create_rectangle(21, 216, 41, 236, fill='#2980b9')

lab_life = Label(frame_controls, text='Punkty życia:', font=('courier new', 13))
lab_life.place(x=27, y=67)



sl_nb_1 = Scale(frame_controls, orient=HORIZONTAL, from_=1, to=8, command=lambda x : set_nb(x, 0))
sl_nb_1.set(NB[0])
sl_nb_1.place(x=190, y=95)

sl_nb_2 = Scale(frame_controls, orient=HORIZONTAL, from_=1, to=8, command=lambda x : set_nb(x, 1))
sl_nb_2.set(NB[1])
sl_nb_2.place(x=190, y=145)

sl_nb_3 = Scale(frame_controls, orient=HORIZONTAL, from_=1, to=8, command=lambda x : set_nb(x, 2))
sl_nb_3.set(NB[2])
sl_nb_3.place(x=190, y=195)

lab_nb = Label(frame_controls, text='Sąsiedzi:', font=('courier new', 13))
lab_nb.place(x=195, y=67)



sl_sf_1 = Scale(frame_controls, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_spawn(x, 0))
sl_sf_1.set(SPAWN[0])
sl_sf_1.place(x=320, y=95)

sl_sf_2 = Scale(frame_controls, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_spawn(x, 1))
sl_sf_2.set(SPAWN[1])
sl_sf_2.place(x=320, y=145)

sl_sf_3 = Scale(frame_controls, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_spawn(x, 2))
sl_sf_3.set(SPAWN[2])
sl_sf_3.place(x=320, y=195)

lab_sf = Label(frame_controls, text='Reprodukcja:', font=('courier new', 13))
lab_sf.place(x=310, y=67)



lab_ctrl = Label(frame_controls, text='Rozgrywka:', font=('courier new', 13))
lab_ctrl.place(x=515, y=67)

lab_tempo = Label(frame_controls, text='Tempo:', font=('courier new', 13))
lab_tempo.place(x=470, y=114)

lab_eq = Label(frame_controls, text='Quake:', font=('courier new', 13))
lab_eq.place(x=470, y=164)

lab_mut = Label(frame_controls, text='Mutacje:', font=('courier new', 13))
lab_mut.place(x=450, y=214)

sl_tempo = Scale(frame_controls, orient=HORIZONTAL, from_=1, to=10, command=lambda x : set_tempo(x))
sl_tempo.set(TEMPO)
sl_tempo.place(x=545, y=95)

sl_eq = Scale(frame_controls, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_sub_it(x))
sl_eq.set(QUAKE)
sl_eq.place(x=545, y=145)

sl_mut = Scale(frame_controls, orient=HORIZONTAL, from_=0, to=10, command=lambda x : set_rand_it(x))
sl_mut.set(MUT)
sl_mut.place(x=545, y=195)

new_board()
clear_all()

root.mainloop()

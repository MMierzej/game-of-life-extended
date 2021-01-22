#!/usr/bin/env python3
from tkinter import *
from logic import *
import platform


LIFE = [2, 4, 6]
NB = [4, 3, 3]
SPAWN = [1, 3, 6]
QUAKE = 5
MUT = 0
REP = 4
TEMPO = 8

# zmienne wielkości okna
x = 10
y = 10
height = y * 30
width = x * 30
fwidth = width + 100 if width > 600 else 700
fheight = height + 350

counter = 0
board = [[[0, 0] for i in range(x)] for j in range(y)]
prev = cp.deepcopy(board)
board_d = dd(lambda : 0)
neighbours_d = dd(lambda : 0)
run = True

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
    
    draw_board()

def clicked_right(event):
    x_click = event.x // 30
    y_click = event.y // 30

    t = board[y_click][x_click][0]
    if t == 1:
        board[y_click][x_click][1] = (1 + board[y_click][x_click][1]) % LIFE[0]
    elif t == 2:
        board[y_click][x_click][1] = (1 + board[y_click][x_click][1]) % LIFE[1]
    elif t == 3:
        board[y_click][x_click][1] = (1 + board[y_click][x_click][1]) % LIFE[2]

    if board[y_click][x_click][1] == 0:
        board[y_click][x_click][0] = 0
    
    draw_board()

def draw_board():
    """rysuje planszę"""
    board_gui.delete("all")

    for y_1 in range(y):
        for x_1 in range(x):
            if board[y_1][x_1][0] == 3:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#ef7c27',
                                           tags=f'{y_1},{x_1}')
            elif board[y_1][x_1][0] == 2:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#009C11',
                                           tags=f'{y_1},{x_1}')
            elif board[y_1][x_1][0] == 1:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#6699ff',
                                           tags=f'{y_1},{x_1}')
            else:
                board_gui.create_rectangle(30 * x_1 + 3, 30 * y_1 + 3, 20 + 30 * x_1 + 3, 20 + 30 * y_1 + 3,
                                           fill='#e3e3e3',
                                           tags=f'{y_1},{x_1}')
            board_gui.tag_bind(f'{y_1},{x_1}', '<Button-1>', clicked_left)
            board_gui.tag_bind(f'{y_1},{x_1}', '<Button-3>', clicked_right)
    
    board_gui.update()


def clear():
    global board_d
    global neighbours_d
    global counter

    for x_1 in range(x):
        for y_1 in range(y):
            board[y_1][x_1][0] = 0
            board[y_1][x_1][1] = 0
    
    board_d = dd(lambda: 0)
    neighbours_d = dd(lambda: 0)
    counter = 0

    draw_board()

def new_board():
    global board
    global prev

    global board_d
    global neighbours_d

    global counter

    board = generate(x, y, LIFE, SPAWN)
    prev = cp.deepcopy(board)

    board_d = dd(lambda: 0)
    neighbours_d = dd(lambda: 0)

    counter = 0

    draw_board()

def start():
    """rozpoczyna symulacje"""
    button_start.place_forget()
    button_stop.place(x=fwidth // 2 - 175, y=7)

    global run
    run = True

    while run:
        step(1)

def stop():
    global run
    run = False

    button_stop.place_forget()
    button_start.place(x=fwidth // 2 - 175, y=7)

def step(a):
    global counter
    i = 0

    while i < a and not repetition(board_d, board, REP):
        clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
        next_state(board, prev, neighbours_d, counter, LIFE, NB, SPAWN, QUAKE, MUT)  # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1
        draw_board()
        time.sleep(1 - (TEMPO - 1) / 10)
        i += 1

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

# utworzone przyciski
button_generate = Button(frame, width=10, text="Generuj", command=new_board)
button_clear = Button(frame, width=10, text="Wyczyść", command=clear)
button_start = Button(frame, width=10, text="Rozpocznij", command=start)
button_stop = Button(frame, width=10, text="Wstrzymaj", command=stop)

button_next = Button(frame_controls, width=10, text="1 ruch", command=lambda: step(1))
button_next_5 = Button(frame_controls, width=10, text="5 ruchów", command=lambda: step(5))
button_next_10 = Button(frame_controls, width=10, text="10 ruchów", command=lambda: step(10))

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

lab_1 = Label(frame_controls, text='1:', font=('courier new', 15))
lab_1.place(x=20, y=113)
lab_2 = Label(frame_controls, text='2:', font=('courier new', 15))
lab_2.place(x=20, y=163)
lab_3 = Label(frame_controls, text='3:', font=('courier new', 15))
lab_3.place(x=20, y=213)

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
clear()

root.mainloop()

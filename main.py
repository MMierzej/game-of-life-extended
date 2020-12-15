import copy as cp
import random


DIRS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]

def generate(h, w):
    board = [[random.randint(0, 1) for i in range(w)] for j in range(h)]
    return board

def draw(plansza):  # funkcja wypisująca planszę do konsoli
    for i in range(len(plansza)):
        for j in range(len(plansza[i])):
            if plansza[i][j] == 0:
                print('_', end="")
            else:
                print('o', end="")

        print()

def count_neighbours(field, x, y, lx, ly):
    counter = 0

    for dx, dy in DIRS:
        nx = (x + dx) % lx
        ny = (y + dy) % ly
        if field[ny][nx] == 1:
            counter += 1

    return counter

def next_state(prev):
    result = cp.deepcopy(prev)  # next state based on previous state

    ly = len(prev)
    lx = len(prev[0])

    for y in range(ly):
        for x in range(lx):
            neighbours = count_neighbours(prev, x, y, lx, ly)

            if neighbours == 3:
                result[y][x] = 1 
            elif prev[y][x] == 1 and neighbours == 2:
                result[y][x] = 1
            else:
                result[y][x] = 0

    return result

def modify(plansza, x, y): # zmienia stan komórki
    if plansza[x][y] == 1:
        plansza[x][y] = 0
    elif plansza[x][y] == 0:
        plansza[x][y] = 1

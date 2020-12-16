import copy as cp
import random
import time


DIRS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]

def generate(height, width):
    board = [[random.randint(0, 1) for i in range(width)] for j in range(height)]
    return board

def draw(plansza):  # funkcja wypisująca planszę do konsoli
    for i in range(len(plansza)):
        for j in range(len(plansza[i])):
            if plansza[i][j] == 0:
                print('_', end="")
            else:
                print('o', end="")

        print()

# "funkcja prywatna" funkcji next_state
def count_neighbours(field, x, y, lx, ly):
    counter = 0

    for dx, dy in DIRS:
        nx = (x + dx) % lx
        ny = (y + dy) % ly
        if field[ny][nx] == 1:
            counter += 1

    return counter

def clone_board(output_board, input_board):
    """ copies the content of prev to board """
    for i in range(len(prev)):
        for j in range(len(prev[0])):
            output_board[i][j] = input_board[i][j]

def next_state(result, prev):
    # prev - lista list, poprzednia plansza
    # result - następny stan modyfikacja "w miejscu"

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

def modify(plansza, x, y):
    if plansza[y][x] == 1:
        plansza[y][x] = 0
    elif plansza[y][x] == 0:
        plansza[y][x] = 1

if __name__ == "__main__":

    txt = """
    0000000000000000000000
    0000000000000000000000
    0000000000000011100000
    0000000000000000000000
    0000000000000000000000
    0000000000000000000000
    0000000000000000000000
    0011100000000000000000
    0000100000000000000000
    0001000000000000000000
    0000000000000000000000
    """

    height = 15
    width = 10
    # board = generate(height, width)
    board = [ [ int(c) for c in wiersz ] for wiersz in txt.split() ]
    prev = cp.deepcopy(board)
    counter = 0
    interval = 1
    
    while counter < 150:
        if counter % interval == 0:
            draw(board)
            print("\n*****************************\n")
            time.sleep(0.1)

        clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
        next_state(board, prev)   # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1

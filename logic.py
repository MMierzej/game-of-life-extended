import copy as cp
import random
import time
from collections import defaultdict as dd


""" stałe """
HEIGHT = 10
WIDTH = 10
DIRS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
LIFE_1 = 2
LIFE_2 = 4
LIFE_3 = 6
NB_1 = 4
NB_2 = 3
NB_3 = 3
SUB_IT = 6
RAND_IT = 4

def generate():  
    """generuje losową planszę z komorkami"""
    
    # board[wiersz][kolumna][0] - gatunek
    # board[wiersz][kolumna][1] - punkty życia
    board = [[[0, 0] for i in range(WIDTH)] for j in range(HEIGHT)]

    for i in range(HEIGHT):
        for j in range(WIDTH):
            possibility = random.uniform(0.0, 1.0)

            if possibility < 0.7:
                # puste pole
                board[i][j][0] = 0
                board[i][j][1] = 0
            elif 0.7 <= possibility < 0.8:
                # gatunek 1
                board[i][j][0] = 1
                board[i][j][1] = LIFE_1
            elif 0.8 <= possibility < 0.9:
                # gatunek 2
                board[i][j][0] = 2
                board[i][j][1] = LIFE_2
            else:
                # gatunek 3
                board[i][j][0] = 3
                board[i][j][1] = LIFE_3
        
    return board

def repetition(board, board_list):  
    """sprawdza czy plansza się zapętla"""
    string = ""
    for i in range(len(board)):
        for j in range(len(board[i])):
            string += str(board[i][j][0])
            string += str(board[i][j][1])
    if string in board_list:
        board_list.append(string)
        return True
    else:
        board_list.append(string)
        return False

"""
def draw(board):  
    # funkcja wypisująca planszę do konsoli
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][0] == 0:
                print(' ', end="")
            elif board[i][j][0] == 1:
                print('o', end="")
            elif board[i][j][0] == 2:
                print('x', end="")
            elif board[i][j][0] == 3:
                print('@', end="")
        print()
"""

def draw(board):  
    """funkcja wypisująca planszę do konsoli do testowania"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][0] == 0:
                print('  ', end=" ")
            elif board[i][j][0] == 1:
                print(f'o{board[i][j][1]}', end=" ")
            elif board[i][j][0] == 2:
                print(f'x{board[i][j][1]}', end=" ")
            elif board[i][j][0] == 3:
                print(f'@{board[i][j][1]}', end=" ")
        print()


def count_neighbours(field, x, y, lx, ly):
    """ "funkcja prywatna" funkcji next_state"""
    neighbours_d = dd(lambda : 0)
    for dx, dy in DIRS:
        nx = (x + dx) % lx
        ny = (y + dy) % ly
        neighbours_d[field[ny][nx][0]] += 1
    return neighbours_d

def clone_board(output_board, input_board):
    """ copies the content of prev to board """
    for i in range(len(prev)):
        for j in range(len(prev[0])):
            output_board[i][j][0] = input_board[i][j][0]
            output_board[i][j][1] = input_board[i][j][1]

def next_state(result, prev, counter):
    """ prev - lista list, poprzednia plansza
    result - następny stan modyfikacja "w miejscu" """

    ly = len(prev)
    lx = len(prev[0])

    for y in range(ly):
        for x in range(lx):
            cell_type = prev[y][x][0]
            nb_d = count_neighbours(prev, x, y, lx, ly)

            if cell_type == 0:
                if nb_d[1] >= NB_1 and nb_d[3] < NB_3:
                    result[y][x][0] = 1
                    result[y][x][1] = LIFE_1

                elif nb_d[1] < NB_1 and nb_d[2] >= NB_2 and counter % 3 == 2:
                    result[y][x][0] = 2
                    result[y][x][1] = LIFE_2

                elif nb_d[2] < NB_2 and nb_d[3] >= NB_3 and counter % 6 == 5:
                    result[y][x][0] = 3
                    result[y][x][1] = LIFE_3

            elif cell_type == 1:
                if nb_d[3] > 0:
                    result[y][x][1] -= 1
                
                if nb_d[2] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < LIFE_1 else LIFE_1

            elif cell_type == 2:
                if nb_d[1] > 0:
                    result[y][x][1] -= 1

                if nb_d[3] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < LIFE_2 else LIFE_2

            elif cell_type == 3:
                if nb_d[2] > 0:
                    result[y][x][1] -= 1

                if nb_d[1] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < LIFE_3 else LIFE_3

            if counter % SUB_IT == SUB_IT - 1:
                result[y][x][1] -= 1

            # eliminacja zdechłych
            if result[y][x][1] <= 0:
                result[y][x][0] = 0
                result[y][x][1] = 0

    # generowanie mutacji losowej komórki podczas gry
    if counter % RAND_IT == RAND_IT - 1:
        rx = random.randint(0, WIDTH - 1)
        ry = random.randint(0, HEIGHT - 1)
        t = random.randint(0, 3)
        result[ry][rx][0] = t
        if t == 0:
            result[ry][rx][1] = 0
        elif t == 1:
            result[ry][rx][1] = LIFE_1
        elif t == 2:
            result[ry][rx][1] = LIFE_2
        else:
            result[ry][rx][1] = LIFE_3

def modify(board, x, y):
    if board[y][x] == 1:
        board[y][x] = 0
    elif board[y][x] == 0:
        board[y][x] = 1


if __name__ == "__main__":
    # board = generate()
    board = [[[0, 0], [0, 0], [0, 0], [3, 7], [0, 0], [0, 0], [0, 0], [2, 5], [0, 0], [0, 0]], [[2, 5], [0, 0], [0, 0], [2, 5], [2, 5], [3, 7], [1, 2], [0, 0], [1, 2], [3, 7]], [[2, 5], [0, 0], [0, 0], [0, 0], [3, 7], [0, 0], [1, 2], [2, 5], [0, 0], [0, 0]], [[3, 7], [0, 0], [1, 2], [0, 0], [3, 7], [0, 0], [0, 0], [2, 5], [0, 0], [0, 0]], [[1, 2], [3, 7], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [3, 7], [0, 0], [0, 0], [2, 5]], [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [2, 5], [3, 7], [0, 0], [0, 0], [0, 0]], [[0, 0], [0, 0], [0, 0], [1, 2], [1, 2], [0, 0], [0, 0], [0, 0], [2, 5], [0, 0]], [[2, 5], [2, 5], [0, 0], [0, 0], [1, 2], [0, 0], [0, 0], [2, 5], [1, 2], [0, 0]], [[0, 0], [0, 0], [1, 2], [0, 0], [1, 2], [0, 0], [1, 2], [0, 0], [0, 0], [0, 0]]]
    prev = cp.deepcopy(board)
    counter = 0
    interval = 1
    board_list = []
    
    print("\n*****************************\n")
    while counter < 200:
        if repetition(board, board_list) == True:
            draw(board)
            print("\n*****************************\n")
            print("Symulacja się zapętliła.")
            break
        else:
            repetition(board, board_list)
            if counter % interval == 0:
                draw(board)
                print("\n*****************************\n")
                time.sleep(0.5)
        clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
        next_state(board, prev, counter)   # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1

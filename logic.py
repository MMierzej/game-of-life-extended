#!/usr/bin/env python3
import copy as cp
import random
import time
from collections import defaultdict as dd


""" stałe """
DIRS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]


def generate(width, height, LIFE, SPAWN):
    """generuje losową planszę z komorkami"""

    # board[wiersz][kolumna][0] - gatunek
    # board[wiersz][kolumna][1] - punkty życia
    board = [[[0, 0] for i in range(width)] for j in range(height)]

    for i in range(height):
        for j in range(width):
            p = random.uniform(0.0, 1.0)

            if 0.7 <= p < 0.8 and SPAWN[0] != 0:
                # gatunek 1
                board[i][j][0] = 1
                board[i][j][1] = LIFE[0]
            elif 0.8 <= p < 0.9 and SPAWN[1] != 0:
                # gatunek 2
                board[i][j][0] = 2
                board[i][j][1] = LIFE[1]
            elif 0.9 <= p and SPAWN[2] != 0:
                # gatunek 3
                board[i][j][0] = 3
                board[i][j][1] = LIFE[2]

    return board


def repetition(board_d, board, REPS):
    """ sprawdza czy plansza się zapętla """
    string = str(board)
    board_d[string] += 1

    if board_d[string] > REPS:
        return True

    return False


def count(board):
    """Funkcja zliczająca powtórzenia komórek"""
    c_1 = 0
    c_2 = 0
    c_3 = 0

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j][0] == 1:
                c_1 += 1
            elif board[i][j][0] == 2:
                c_2 += 1
            elif board[i][j][0] == 3:
                c_3 += 1
    print('Ilość wystąpień komórek: o:', c_1, 'x:', c_2, '@:', c_3)


def draw(board):
    """funkcja wypisująca planszę do konsoli do testowania"""
    print("\n*****************************\n")

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

    print("\n*****************************\n")


def count_neighbours(board, neighbours_d, x, y):
    """ "funkcja prywatna" funkcji next_state """
    for i in range(4):
        neighbours_d[i] = 0

    for dx, dy in DIRS:
        nx = (x + dx) % len(board[0])
        ny = (y + dy) % len(board)
        neighbours_d[board[ny][nx][0]] += 1

    return neighbours_d


def clone_board(output_board, input_board):
    """ kopiowanie zawartości input do output """
    for i in range(len(input_board)):
        for j in range(len(input_board[0])):
            output_board[i][j][0] = input_board[i][j][0]
            output_board[i][j][1] = input_board[i][j][1]


def next_state(result, prev, neighbours_d, counter, LIFE, NB, SPAWN, SUB_IT, RAND_IT):
    """
    prev - lista list, poprzednia plansza
    result - następny stan modyfikacja "w miejscu"
    """

    for y in range(len(prev)):
        for x in range(len(prev[0])):
            cell_type = prev[y][x][0]
            nb_d = count_neighbours(prev, neighbours_d, x, y)

            if SUB_IT != 0 and counter % SUB_IT == SUB_IT - 1:
                result[y][x][1] -= 1

            if cell_type == 0:
                if SPAWN[0] != 0 and nb_d[1] >= NB[0] and nb_d[3] < NB[2] and counter % SPAWN[0] == SPAWN[0] - 1:
                    result[y][x][0] = 1
                    result[y][x][1] = LIFE[0]

                elif SPAWN[1] != 0 and nb_d[1] < NB[0] and nb_d[2] >= NB[1] and counter % SPAWN[1] == SPAWN[1] - 1:
                    result[y][x][0] = 2
                    result[y][x][1] = LIFE[1]

                elif SPAWN[2] != 0 and nb_d[2] < NB[1] and nb_d[3] >= NB[2] and counter % SPAWN[2] == SPAWN[2] - 1:
                    result[y][x][0] = 3
                    result[y][x][1] = LIFE[2]

            elif cell_type == 1:
                if nb_d[3] > 0:
                    result[y][x][1] -= 1

                if nb_d[2] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < LIFE[0] else LIFE[0]

            elif cell_type == 2:
                if nb_d[1] > 0:
                    result[y][x][1] -= 1

                if nb_d[3] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < LIFE[1] else LIFE[1]

            elif cell_type == 3:
                if nb_d[2] > 0:
                    result[y][x][1] -= 1

                if nb_d[1] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < LIFE[2] else LIFE[2]

            # eliminacja zdechłych
            if result[y][x][1] <= 0:
                result[y][x][0] = 0
                result[y][x][1] = 0

    """ generowanie mutacji losowej komórki """
    if RAND_IT != 0 and counter % RAND_IT == RAND_IT - 1:
        rx = random.randint(0, len(prev[0]) - 1)
        ry = random.randint(0, len(prev) - 1)
        t = random.randint(0, 3)

        result[ry][rx][0] = t

        if t == 0:
            result[ry][rx][1] = 0
        elif t == 1:
            result[ry][rx][1] = LIFE[0]
        elif t == 2:
            result[ry][rx][1] = LIFE[1]
        else:
            result[ry][rx][1] = LIFE[2]


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


# if __name__ == "__main__":
#     # board = generate(HEIGHT, WIDTH)
#     board = [[[0, 0], [0, 0], [0, 0], [3, 6], [0, 0], [0, 0], [0, 0], [2, 4], [0, 0], [0, 0]],
#              [[2, 4], [0, 0], [0, 0], [2, 4], [2, 4], [3, 6], [1, 2], [0, 0], [1, 2], [3, 6]],
#              [[2, 4], [0, 0], [0, 0], [0, 0], [3, 6], [0, 0], [1, 2], [2, 4], [0, 0], [0, 0]],
#              [[3, 6], [0, 0], [1, 2], [0, 0], [3, 6], [0, 0], [0, 0], [2, 4], [0, 0], [0, 0]],
#              [[1, 2], [3, 6], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
#              [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [3, 6], [0, 0], [0, 0], [2, 4]],
#              [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [2, 4], [3, 6], [0, 0], [0, 0], [0, 0]],
#              [[0, 0], [0, 0], [0, 0], [1, 2], [1, 2], [0, 0], [0, 0], [0, 0], [2, 4], [0, 0]],
#              [[2, 4], [2, 4], [0, 0], [0, 0], [1, 2], [0, 0], [0, 0], [2, 4], [1, 2], [0, 0]],
#              [[0, 0], [0, 0], [1, 2], [0, 0], [1, 2], [0, 0], [1, 2], [0, 0], [0, 0], [0, 0]]]
#     prev = cp.deepcopy(board)
#     board_d = dd(lambda: 0)
#     neighbours_d = dd(lambda: 0)
#     counter = 0

#     while counter < 1000 and not repetition(board_d, board):
#         if counter % REFRESH_IT == 0:
#             draw(board)
#             count(board)
#             time.sleep(0.2)

#         clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
#         next_state(board, prev, neighbours_d, counter)  # ta funkcja generuje następny stan planszy (do zmiennej board)
#         counter += 1

#     draw(board)
#     count(board)
#     print("Symulacja się zapętliła." if counter < 1000 else "Koniec.")

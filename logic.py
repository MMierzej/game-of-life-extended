import copy as cp
import random
import time
from collections import defaultdict as dd


DIRS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]

def generate(height, width):  
    """generuje losową planszę z komorkami"""
    board = [[[random.randint(0, 3), 0] for i in range(width)] for j in range(height)]

    for row in board:
        for cell in row:
            if cell[0] == 1:
                cell[1] = 3
            elif cell[0] == 2:
                cell[1] = 7
            elif cell[0] == 3:
                cell[1] = 10
    
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

def draw(board):  
    """funkcja wypisująca planszę do konsoli"""
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
                if nb_d[1] >= 3 and nb_d[3] < 1:
                    result[y][x][0] = 1
                    result[y][x][1] = 3
                elif nb_d[1] < 3 and nb_d[2] >= 2 and counter % 3 == 0:
                    result[y][x][0] = 2
                    result[y][x][1] = 7 
                elif nb_d[2] < 2 and nb_d[3] >= 1 and counter % 6 == 0:
                    result[y][x][0] = 3
                    result[y][x][1] = 10 
            elif cell_type == 1:
                if nb_d[2] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < 3 else 3
                if nb_d[3] > 0:
                    result[y][x][1] -= 1
            elif cell_type == 2:
                if nb_d[3] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < 7 else 7
                if nb_d[1] > 0:
                    result[y][x][1] -= 1
            elif cell_type == 3:
                if nb_d[1] > 0:
                    result[y][x][1] = prev[y][x][1] + 1 if prev[y][x][1] < 10 else 10
                if nb_d[2] > 0:
                    result[y][x][1] -= 1
            
            # eliminacja zdechłych
            if result[y][x][1] <= 0:
                result[y][x][0] = 0
                result[y][x][1] = 0

def modify(board, x, y):
    if board[y][x] == 1:
        board[y][x] = 0
    elif board[y][x] == 0:
        board[y][x] = 1


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
    board = generate(height, width)
    # board = [ [ int(c) for c in wiersz ] for wiersz in txt.split() ]
    prev = cp.deepcopy(board)
    counter = 0
    interval = 5
    board_list = []
    while counter < 150:
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
                time.sleep(0.2)
        clone_board(prev, board)  # ta funkcja modyfikuje prev, zachowujemy tu stan planszy przed nową iteracją
        next_state(board, prev, counter)   # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1

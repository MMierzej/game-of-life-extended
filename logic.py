import copy as cp
import random
import time

DIRS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]


def generate(height, width):  
    """generuje losową planszę z komorkami"""
    board = [[random.randint(0, 3) for i in range(width)] for j in range(height)]
    return board


def repetition(board, board_list):  
    """sprawdza czy plansza się zapętla"""
    string = ""
    for i in range(len(board)):
        for j in range(len(board[i])):
            string += str(board[i][j])

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
            if board[i][j] == 0:
                print(' ', end="")
            elif board[i][j] == 1:
                print('o', end="")
            elif board[i][j] == 2:
                print('x', end="")
            elif board[i][j] == 3:
                print('@', end="")

        print()


def count_neighbours(field, x, y, lx, ly):
    """ "funkcja prywatna" funkcji next_state"""
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
    """ prev - lista list, poprzednia plansza
    result - następny stan modyfikacja "w miejscu" """
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
        next_state(board, prev)  # ta funkcja generuje następny stan planszy (do zmiennej board)
        counter += 1

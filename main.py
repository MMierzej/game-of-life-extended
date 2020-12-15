import copy as cp


DIRS = [ (-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1) ]

# def show(state):
#     for i in range(len(state)):
#         for c in state[i]:
#             print(c, end=' ')
        
#         print()

def count_neighbours(field, x, y, lx, ly):
    counter = 0

    for dx, dy in DIRS:
        nx = (x + dx) % lx
        ny = (y + dy) % ly
        if field[ny][nx] == 'o':
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
                result[y][x] = 'o'
            elif prev[y][x] == 'o' and neighbours == 2:
                result[y][x] = 'o'
            else:
                result[y][x] = '_'

    return result


# txt = """
# ______________________
# ______________________
# ______________ooo_____
# ______________________
# ______________________
# ______________________
# ______________________
# __ooo_________________
# ____o_________________
# ___o__________________
# ______________________
# """

# prev = [ list(wiersz) for wiersz in txt.split() ]

# show(prev)
# for _ in range(10):
#     curr = next_state(prev)
#     print()
#     print()
#     show(curr)
#     prev = curr

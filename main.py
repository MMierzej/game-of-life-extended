import random


def draw(plansza):  # Funkcja wypisująca planszę do konsoli

    for i in range(len(plansza)):
        for j in range(len(plansza[i])):
            if plansza[i][j] == 0:
                print('_', end="")
            else:
                print('o', end="")
        print("")


l = []
a = [0, 1]
for i in range(10):
    l.append([])
    for j in range(10):
        l[i].append(random.choice(a))

draw(l)

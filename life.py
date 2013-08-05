from collections import Counter
from itertools import product

def adjacent_points(point):
    for x, y in product((-1, 0, 1), (-1, 0, 1)):
        if (x, y) != (0, 0):
            yield (point[0] + x, point[1] + y)

def cell_age(point, old_board):
    alive_neighbours = sum(bool(old_board[p]) for p in adjacent_points(point))
    if alive_neighbours == 3:
        return old_board[point] + 1
    elif alive_neighbours == 2 and old_board[point]:
        return old_board[point] + 1
    else:
        return 0

def update_cell(point, new_board, old_board):
    alive = cell_age(point, old_board)
    if alive:
        new_board[point] = alive

def next_iteration(old_board):
    new_board = Counter()
    for point in old_board:
        update_cell(point, new_board, old_board)
        for p in adjacent_points(point):
            if p not in old_board:
                update_cell(p, new_board, old_board)
    return new_board

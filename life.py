from collections import Counter, namedtuple

class Point(namedtuple('Point', 'x y')):
    __slots__ = ()

    def __add__(self, other):
        try:
            return self.__class__(
                    self.x + other[0],
                    self.y + other[1])
        except IndexError:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        try:
            return self.__class__(
                    self.x - other[0],
                    self.y - other[1])
        except IndexError:
            return NotImplemented

    def __rsub__(self, other):
        try:
            return self.__class__(
                    other[0] - self.x,
                    other[1] - self.y)
        except IndexError:
            return NotImplemented

    def __mul__(self, other):
        try:
            return self.__class__(self.x*other, self.y*other)
        except TypeError:
            return NotImplemented

    def __rmul__(self, other):
        return self*other

    def __floordiv__(self, other):
        try:
            return self.__class__(
                    int(self.x // other),
                    int(self.y // other))
        except TypeError:
            return NotImplemented

    def rotate(self, angle):
        x, y = self
        if angle == 90:
            return Point(-y, x)
        elif angle == 180:
            return Point(-x, -y)
        elif angle == 270:
            return Point(y, -x)
        else:
            return ValueError('Angle must be 90, 180 or 270')

    @property
    def adjacent(self):
        return {self + (-1, -1), self + (-1, 0), self + (-1, 1),
                self + (0, -1), self + (0, 1),
                self + (1, -1), self + (1, 0), self + (1, 1)}

def cell_age(point, old_board):
    alive_neighbours = len([1 for p in point.adjacent if old_board[p]])
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
    points = {p for p in old_board}
    for point in old_board:
        points.update(point.adjacent)

    for point in points:
        update_cell(point, new_board, old_board)
    return new_board

def parse_life_1_06(pattern_file):
    cells = set()
    next(pattern_file) # Remove unwanted header
    for line in pattern_file:
        cells.add(Point(*[int(i) for i in line.split()]))
    return normalise(cells)

def normalise(cells):
    min_x = min(cell.x for cell in cells)
    min_y = min(cell.y for cell in cells)
    return {cell - (min_x, min_y) for cell in cells}

def rotate(cells, angle):
    return {cell.rotate(angle) for cell in cells}



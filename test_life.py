from collections import Counter

from life import next_iteration, normalise, rotate, Point

class TestPoint:
    def test_access(self):
        point = Point(0, 1)
        assert point.x == 0
        assert point.y == 1
        assert point[0] == 0
        assert point[1] == 1

    def test_add(self):
        point = Point(0, 1)
        assert point + Point(3, 1) == Point(3, 2)

        assert point + (-1, 2) == Point(-1, 3)

        assert (-1, 2) + point == Point(-1, 3)

    def test_subtract(self):
        assert Point(3, 1) - Point(0, 1) == Point(3, 0)
        assert Point(3, 1) - (0, 1) == Point(3, 0)
        assert (3, 1) - Point(0, 1) == Point(3, 0)

    def test_rotate(self):
        point = Point(2, 1)
        assert point.rotate(90) == Point(-1, 2)
        assert point.rotate(180) == Point(-2, -1)
        assert point.rotate(270) == Point(1, -2)

    def test_adjacent(self):
        point = Point(3, 2)
        adjacent = {Point(2, 1), Point(2, 2), Point(2, 3),
                Point(3, 1), Point(3, 3),
                Point(4, 1), Point(4, 2), Point(4, 3)}
        assert point.adjacent == adjacent

    def test_multiply(self):
        point = Point(4, 5)
        assert point*10 == Point(40, 50)
        assert 10*point == Point(40, 50)

    def test_floordiv(self):
        point = Point(25, 18)
        assert point // 7 == Point(3, 2)

class TestBoard:
    def test_empty(self):
        board = Counter()
        new_board = next_iteration(board)
        assert new_board == Counter()

    def test_one(self):
        board = Counter({Point(0, 0): 1})
        new_board = next_iteration(board)
        assert new_board == Counter()

    def test_square(self):
        board = Counter({
            Point(0, 0): 1,
            Point(0, 1): 1,
            Point(1, 0): 1,
            Point(1, 1): 1,
            })

        new_board = next_iteration(board)
        assert new_board == Counter({
            Point(0, 0): 2,
            Point(0, 1): 2,
            Point(1, 0): 2,
            Point(1, 1): 2,
            })

    def test_line(self):
        board_0 = Counter({
            Point(0, 0): 1,
            Point(0, 1): 1,
            Point(0, 2): 1,
            })

        board_1 = next_iteration(board_0)
        assert board_1 == Counter({
            Point(-1, 1): 1,
            Point(0, 1): 2,
            Point(1, 1): 1,
            })

        board_2 = next_iteration(board_1)
        assert board_2 == Counter({
            Point(0, 0): 1,
            Point(0, 1): 3,
            Point(0, 2): 1,
            })

def test_normalise():
    pattern = {Point(0, 0), Point(1, 0), Point(0, 1), Point(2, 1)}
    assert normalise(pattern) == pattern

    pattern = {Point(-1, 0), Point(2, 0), Point(0, 1)}
    assert normalise(pattern) == {Point(0, 0), Point(3, 0), Point(1, 1)}

    pattern = {Point(-2, -3), Point(-4, -2), Point(4, 5)}
    assert normalise(pattern) == {Point(2, 0), Point(0, 1), Point(8, 8)}

def test_rotate():
    pattern = {Point(0, 0), Point(1, 0), Point(0, 1), Point(2, 1)}

    pattern_90 = rotate(pattern, 90)
    assert pattern_90 == {Point(0, 0), Point(0, 1), Point(-1, 0), Point(-1, 2)}

    pattern_180 = rotate(pattern, 180)
    assert pattern_180 == {Point(0, 0), Point(-1, 0), Point(0, -1), Point(-2, -1)}

    pattern_270 = rotate(pattern, 270)
    assert pattern_270 == {Point(0, 0), Point(0, -1), Point(1, 0), Point(1, -2)}


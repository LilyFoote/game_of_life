from collections import Counter

from life import next_iteration, normalise, rotate

class TestBoard:
    def test_empty(self):
        board = Counter()
        new_board = next_iteration(board)
        assert new_board == Counter()

    def test_one(self):
        board = Counter({(0, 0): 1})
        new_board = next_iteration(board)
        assert new_board == Counter()

    def test_square(self):
        board = Counter({
            (0, 0): 1,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 1,
            })

        new_board = next_iteration(board)
        assert new_board == Counter({
            (0, 0): 2,
            (0, 1): 2,
            (1, 0): 2,
            (1, 1): 2,
            })

    def test_line(self):
        board_0 = Counter({
            (0, 0): 1,
            (0, 1): 1,
            (0, 2): 1,
            })

        board_1 = next_iteration(board_0)
        assert board_1 == Counter({
            (-1, 1): 1,
            (0, 1): 2,
            (1, 1): 1,
            })

        board_2 = next_iteration(board_1)
        assert board_2 == Counter({
            (0, 0): 1,
            (0, 1): 3,
            (0, 2): 1,
            })

def test_normalise():
    pattern = {(0, 0), (1, 0), (0, 1), (2, 1)}
    assert normalise(pattern) == pattern

    pattern = {(-1, 0), (2, 0), (0, 1)}
    assert normalise(pattern) == {(0, 0), (3, 0), (1, 1)}

    pattern = {(-2, -3), (-4, -2), (4, 5)}
    assert normalise(pattern) == {(2, 0), (0, 1), (8, 8)}

def test_rotate():
    pattern = {(0, 0), (1, 0), (0, 1), (2, 1)}

    pattern_90 = rotate(pattern, 90)
    assert pattern_90 == {(0, 0), (0, 1), (-1, 0), (-1, 2)}

    pattern_180 = rotate(pattern, 180)
    assert pattern_180 == {(0, 0), (-1, 0), (0, -1), (-2, -1)}

    pattern_270 = rotate(pattern, 270)
    assert pattern_270 == {(0, 0), (0, -1), (1, 0), (1, -2)}


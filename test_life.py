from collections import Counter

from life import next_iteration

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


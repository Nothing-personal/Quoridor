from unittest import TestCase
from sample import Tile, Player, Board


class TestBoard(TestCase):

    def test_init(self):
        board = Board()
        # Checking board size
        self.assertEqual(len(board.field), 9)
        for i in board.field:
            self.assertEqual(len(i), 9)

    def test_neighbours(self):
        board = Board()
        self.assertEqual(board.field[0][0].neighbours, [board.field[1][0], board.field[0][1]])

    def test_get_tile(self):
        board = Board()
        self.assertEqual(board.get_tile(1, 2), board.field[1][2])

    def test_walls(self):
        board = Board()
        player = Player(1, board)
        player.place_wall([board.field[1][2], board.field[1][3], board.field[2][2], board.field[2][3]], "hor")
        self.assertTrue(board.field[1][2] not in board.field[2][2].neighbours)
        self.assertTrue(board.field[2][2] not in board.field[1][2].neighbours)
        self.assertTrue(board.field[1][3] not in board.field[2][3].neighbours)
        self.assertTrue(board.field[2][3] not in board.field[1][3].neighbours)

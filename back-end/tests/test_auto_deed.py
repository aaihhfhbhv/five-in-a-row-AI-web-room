import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auto_deed import get_auto_move


class AutoDeedTestCase(unittest.TestCase):
    def test_prefers_winning_move(self):
        states = {0: 1, 1: 1, 2: 1, 3: 1}
        move = get_auto_move(states, 1, 8, 8, 5)
        self.assertEqual(move, 4)

    def test_blocks_immediate_opponent_win(self):
        states = {0: 2, 1: 2, 2: 2, 3: 2}
        move = get_auto_move(states, 1, 8, 8, 5)
        self.assertEqual(move, 4)


if __name__ == '__main__':
    unittest.main()

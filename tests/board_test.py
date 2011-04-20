import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
import random
from starjeweled import *

class BoardTestCase(unittest.TestCase):
    def testMoveClass(self):
        m = Move(0, 1, 2, 3)
        self.assertEqual(m.src['x'], 0, 'move src x')
        self.assertEqual(m.src['y'], 1, 'move src y')
        self.assertEqual(m.des['x'], 2, 'move des x')
        self.assertEqual(m.des['y'], 3, 'move des y')

    def testBoardInitialization(self):
        b = Board()
        self.assertEqual(b.num_rows, 8, 'checking rows')
        self.assertEqual(b.num_cols, 8, 'checking cols')

    def testBoardNoMovesFound(self):
        b = Board()
        b.setBoard("0" * b.num_rows * b.num_cols)
        self.assertEqual(b.findMove(), None, 'checking no moves found')

        b.setBoard("00b0b000" + ("0" * 7 * 8))
        self.assertEqual(b.findMove(), None, 'checking no moves found')

    def testBoardArrayMethods(self):
        b = Board()

        b.board = ""
        for i in range(b.num_cols * b.num_rows):
            b.board = b.board + str(random.randint(0, 9))
        orig_board = b.board

        self.assertEqual(orig_board, b.fromArray(b.toArray()), 'checking fromArray and toArray methods')
if __name__ == '__main__':
    unittest.main()

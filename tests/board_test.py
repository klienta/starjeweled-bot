import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
import random
from starjeweled import *

class BoardTestCase(unittest.TestCase):
    def setUp(self):
        self.b = Board()
        
    def testBoardInitialization(self):
        self.assertEqual(self.b.num_rows, 8, 'checking rows')
        self.assertEqual(self.b.num_cols, 8, 'checking cols')

    def testBoardArrayMethods(self):
        self.b.board = ""
        for i in range(self.b.num_cols * self.b.num_rows):
            self.b.board = self.b.board + str(random.randint(0, 9))
        orig_board = self.b.board

        self.assertEqual(orig_board, self.b.fromArray(self.b.toArray()), 'checking fromArray and toArray methods')
if __name__ == '__main__':
    unittest.main()

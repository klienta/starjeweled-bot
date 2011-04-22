import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
import random
from move import *
from starjeweled import *
from strategy import *

class AiTestCase(unittest.TestCase):
    def setUp(self):
        self.b = Board()
        self.strategy = Strategy( self.b )
      
    def testNoMovesFound(self):
        self.b.setBoard("0" * self.b.num_rows * self.b.num_cols)
        self.assertEqual(self.strategy.findMove(), None, 'checking no moves found')

        self.b.setBoard("00b0b000" + ("0" * 7 * 8))
        self.assertEqual(self.strategy.findMove(), None, 'checking no moves found')

if __name__ == '__main__':
    unittest.main()

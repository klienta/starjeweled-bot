import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
import random
from move import *
from starjeweled import *
from strategy import *

class StrategyTestCase(unittest.TestCase):
    def setUp(self):
        self.b = Board()
        self.strategy = Strategy( self.b )
      
    def testNoMovesFound(self):
        self.b.setBoard("0" * self.b.num_rows * self.b.num_cols)
        self.assertEqual(self.strategy.findMove(), None, 'checking no moves found')

        self.b.setBoard("00b0b000" + ("0" * 7 * 8))
        self.assertEqual(self.strategy.findMove(), None, 'checking no moves found')

    def testHorizontalThree(self):
        empty_row = list('0' * self.b.num_cols)
        self.b.fromArray([
          list('00000bb0'),
          list('0000000b'),
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
        ])
        self.assertEqual(str(self.strategy.findMove()), '(7, 1) to (7, 0)')
        
        self.b.fromArray([
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          list('00000bb0'),
          list('0000000b'),
        ])
        self.assertEqual(str(self.strategy.findMove()), '(7, 7) to (7, 6)')
        
        self.b.fromArray([
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          list('0000000b'),
          list('b0000000'),
          list('0b00000b'),
        ])
        self.assertEqual(self.strategy.findMove(), None)
        
        self.b.fromArray([
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          list('b0b00000'),
          list('0b000000'),
          empty_row,
        ])
        self.assertEqual(str(self.strategy.findMove()), '(1, 6) to (1, 5)')
        
    def testHorizontalFour(self):
        #provide the opportunity for 3, but it should prefer the 4.
        empty_row = list('0' * self.b.num_cols)
        self.b.fromArray([
          list('000000bb'),
          list('00000b00'),
          list('0000b0bb'),
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
        ])
        self.assertEqual(str(self.strategy.findMove()), '(5, 1) to (5, 2)')
        

    def testVerticalThree(self):
        empty_row = list('0' * self.b.num_cols)
        self.b.fromArray([
          list('0000000b'),
          list('000000b0'),
          list('0000000b'),
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
        ])
        self.assertEqual(str(self.strategy.findMove()), '(6, 1) to (7, 1)')

        self.b.fromArray([
          list('0000000b'),
          list('0000000b'),
          list('000000b0'),
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
        ])
        self.assertEqual(str(self.strategy.findMove()), '(6, 2) to (7, 2)')
        
        self.b.fromArray([
          list('0000000b'),
          list('0000000b'),
          empty_row,
          list('b0000000'),
          empty_row,
          empty_row,
          empty_row,
          empty_row,
          empty_row,
        ])
        self.assertEqual(self.strategy.findMove(), None)
        
    def testScenario(self): 
      self.b.setBoard('pbbyprbyrkbbpggbp')
      self.b.show()
      print(str(self.strategy.findMove()))
      
         
if __name__ == '__main__':
    unittest.main()

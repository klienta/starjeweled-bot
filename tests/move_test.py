import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
import random
from move import *

class MoveTestCase(unittest.TestCase):
    def testMoveClass(self):
        m = Move(0, 1, 2, 3)
        self.assertEqual(m.src['x'], 0, 'move src x')
        self.assertEqual(m.src['y'], 1, 'move src y')
        self.assertEqual(m.des['x'], 2, 'move des x')
        self.assertEqual(m.des['y'], 3, 'move des y')
        self.assertEqual( str(m), "(0, 1) to (2, 3)", 'string conversion test')

if __name__ == '__main__':
    unittest.main()

import unittest

class EmptyTestCase(unittest.TestCase):
    def runTest(self):
        self.assertEqual(True, True, 'testing works')

if __name__ == '__main__':
    unittest.main()

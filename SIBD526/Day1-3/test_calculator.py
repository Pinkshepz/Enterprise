import unittest
from calculator import Calculator

class TestCalculator(unittest.TestCase):

    def test_add(self):
        c = Calculator()
        result = c.add(3, 5)
        self.assertEqual(result, 8)

    def test_subtract(self):
        c = Calculator()
        result = c.subtract(5, 2)
        self.assertEqual(result, 3)

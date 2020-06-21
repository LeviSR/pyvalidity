from unittest import TestCase
import unittest

from pyvalidity.Literal import Literal

# Literal

class TestLiteral(TestCase):
    def setUp(self):
        self.lit = Literal('a', False)
        self.lit_inv = Literal('a', True)


class TestToString(TestLiteral):
    def test_str(self):
        self.assertEqual('a', self.lit.__str__())

    def test_str_inverse(self):
        self.assertEqual('A', self.lit_inv.__str__())


class TestInversion(TestLiteral):
    def test_invert(self):
        self.assertEqual(Literal('a', True), self.lit.inv())
        self.assertEqual(Literal('a', False), self.lit_inv.inv())


if __name__ == '__main__':
    unittest.main()

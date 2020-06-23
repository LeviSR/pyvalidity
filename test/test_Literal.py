from unittest import TestCase
import unittest

from pyvalidity.Literal import Literal

# Literal


class TestLiteral(TestCase):
    def setUp(self):
        self.lit = Literal('a', False)
        self.lit_inv = Literal('a', True)

    def test_equals(self):
        lit1 = Literal('x0')
        lit2 = Literal('x0', True)
        self.assertEqual(lit1, lit2.inv())


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

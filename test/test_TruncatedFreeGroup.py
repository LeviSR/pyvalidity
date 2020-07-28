from unittest import TestCase
import unittest

from Literal import Literal
from TruncatedFreeGroup import TruncatedFreeGroup


class TestTruncatedFreeGroup(TestCase):
    def setUp(self):
        self.literals = {Literal('x'), Literal('y')}

    def test_count(self):
        tr_grp = TruncatedFreeGroup(2, self.literals)
        self.assertEqual(17, len(tr_grp),
                         tr_grp.__str__() + " is not B_2(F(2))")

    def test_one_shorter(self):
        tr_grp = TruncatedFreeGroup(3, self.literals)
        self.assertEqual(17, len(tr_grp.one_shorter()),
                         tr_grp.__str__() + " is not one shorter than B_3(F(3))")


if __name__ == '__main__':
    unittest.main()

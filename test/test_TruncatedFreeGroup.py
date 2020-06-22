from unittest import TestCase
import unittest

from pyvalidity.Literal import Literal
from pyvalidity.TruncatedFreeGroup import TruncatedFreeGroup


class TestTruncatedFreeGroup(TestCase):
    def setUp(self):
        self.literals = {Literal('x'), Literal('y')}

    def test_count(self):
        tr_grp = TruncatedFreeGroup(2, self.literals)
        self.assertEqual(17, len(tr_grp),
                         tr_grp.__str__() + " is not B_2(F(2))")


if __name__ == '__main__':
    unittest.main()

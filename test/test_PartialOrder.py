from unittest import TestCase
import unittest

from Literal import Literal
from PartialOrder import PartialOrder
from MultiplicativelyClosedSet import MultiplicativelyClosedSet
from TruncatedFreeGroup import TruncatedFreeGroup
from GroupTerm import GroupTerm


class TestPartialOrder(TestCase):
    def setUp(self):
        self.max_length = 2
        self.x = GroupTerm([Literal('x')])
        self.y = GroupTerm([Literal('y')])
        self.generators = {Literal('x'), Literal('y')}
        self.truncated_group = TruncatedFreeGroup(self.max_length,
                                                  self.generators)

    def test_extends(self):
        positives = MultiplicativelyClosedSet({self.x, self.y.inv()},
                                              self.max_length)
        order = PartialOrder(positives, self.truncated_group)
        self.assertTrue(order.extends_to_total_order())

    def test_extends2(self):
        positives = MultiplicativelyClosedSet({self.x, self.x.inv()},
                                              self.max_length)
        order = PartialOrder(positives, self.truncated_group)
        self.assertFalse(order.extends_to_total_order())


if __name__ == '__main__':
    unittest.main()

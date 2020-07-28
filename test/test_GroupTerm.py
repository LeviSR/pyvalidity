from unittest import TestCase
import unittest

from GroupTerm import GroupTerm
from Literal import Literal


# GroupTerm
class TestGroupTerm(TestCase):
    def setUp(self) -> None:
        self.lit = Literal('a', False)

    def test_str_identity(self):
        self.assertEqual('e', GroupTerm([]).__str__())

    def test_str(self):
        term = GroupTerm([self.lit, self.lit])
        self.assertEqual("aa", term.__str__())


class TestReduce(TestGroupTerm):
    def test_reduce(self):
        term = GroupTerm([self.lit, self.lit.inv()])
        self.assertEqual(GroupTerm([]), term)

    def test_is_reduced(self):
        term = GroupTerm([self.lit])
        self.assertTrue(term.is_reduced())
        term = GroupTerm([self.lit.inv()])
        self.assertTrue(term.is_reduced())
        term = GroupTerm([])
        self.assertTrue(term.is_reduced())
        term = GroupTerm([self.lit, self.lit])
        self.assertTrue(term.is_reduced())


class TestTimes(TestGroupTerm):
    def test_times(self):
        self.assertEqual(GroupTerm([]),
                         GroupTerm([self.lit]).times(GroupTerm([self.lit]).inv()))


class TestReplace(TestCase):
    def test_replace(self):
        x = Literal('x')
        y = Literal('y')
        z = Literal('z')

        term = GroupTerm([x, y.inv(), z]).replace_under_bijection([x, y, z], [z, x, y])
        string = str(term)
        self.assertEqual(GroupTerm([z, x.inv(), y]), term,
                         "expected zXy but got " + str(term))


if __name__ == '__main__':
    unittest.main()

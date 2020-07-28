from unittest import TestCase
import unittest

from Parser import Parser
from LGroupTerm import *
from Literal import Literal
from GroupTerm import GroupTerm


# LGroupTerm

class TestAtom(TestCase):
    def setUp(self):
        self.identity = Atom(GroupTerm([]))

    def test_is_identity(self):
        self.assertTrue(self.identity.is_identity())
        self.assertTrue(self.identity.inv().is_identity())

    def test_cnf3(self):
        # self.assertEqual("abx0 v X0cd", Parser("abcd").parse().cnf3())
        string = str(Parser("abcdf").parse().cnf3())
        self.assertTrue("abx0" in string)
        self.assertTrue("X0cx1" in string)
        self.assertTrue("X1df" in string)

        string = str(Parser("abcd v fghi").parse().cnf3())
        self.assertTrue(("abx0" in string and "fgx1" in string) or ("abx1" in string and "fgx0" in string),
                        string + " is not equivalent to abcd v fghi")

    def test_cnf3_edge_cases(self):
        pathological1 = str(Parser("a").parse().cnf3())
        self.assertEqual("a", pathological1)

        pathological2 = str(Parser("ab").parse().cnf3())
        self.assertEqual("ab", pathological2)

        pathological3 = str(Parser("abc").parse().cnf3())
        self.assertEqual("abc", pathological3)


class TestMeet(TestCase):
    def setUp(self):
        self.x = Atom(GroupTerm([Literal('x', False)]))
        self.y = Atom(GroupTerm([Literal('y', False)]))
        self.z = Atom(GroupTerm([Literal('z', False)]))
        self.meet = Meet({self.x, self.y, self.z})

    def test_str(self):
        self.assertRegex(self.meet.__str__(), ". \^ . \^ .")

    def test_absorb(self):
        self.assertEqual(self.meet, Meet(self.meet.meetands))
        self.assertEqual(self.meet,
                         Meet(self.meet.meetands | {self.x}))

    def test_associate(self):
        self.assertEqual(self.meet,
                         Meet({self.x, Meet({self.y, self.z})}))


class TestInverse(TestCase):
    def setUp(self):
        self.x = Atom(GroupTerm([Literal('x')]))
        self.y = Atom(GroupTerm([Literal('y')]))

    def test_inverse(self):
        left = self.x.inv().prod(self.y.inv())
        right = (self.y.prod(self.x)).inv()
        self.assertEqual(left, right, str(left) + " /= " + str(right))
        left = self.x.inv().meet(self.y.inv())
        right = self.x.join(self.y).inv()
        self.assertEqual(left, right, str(left) + " /= " + str(right))
        left = self.x.inv().join(self.y.inv())
        right = self.x.meet(self.y).inv()
        self.assertEqual(left, right, str(left) + " /= " + str(right))

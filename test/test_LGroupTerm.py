from unittest import TestCase
import unittest

from pyvalidity.LGroupTerm import *
from pyvalidity.Literal import Literal
from pyvalidity.GroupTerm import GroupTerm


# LGroupTerm

class TestAtom(TestCase):
    def setUp(self):
        self.identity = Atom(GroupTerm([]))

    def test_is_identity(self):
        self.assertTrue(self.identity.is_identity())
        self.assertTrue(self.identity.inv().is_identity())


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


class TestProduct(TestCase):
    def setUp(self):
        self.x = Atom(GroupTerm([Literal('x')]))
        self.y = Atom(GroupTerm([Literal('y')]))


if __name__ == '__main__':
    unittest.main()

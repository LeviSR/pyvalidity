from unittest import TestCase

from pyvalidity.GroupTerm import GroupTerm
from pyvalidity.LGroupInequation import LGroupInequation
from pyvalidity.LGroupTerm import Atom
from pyvalidity.Literal import Literal


class TestLGroupInequation(TestCase):
    def setUp(self):
        self.x = Atom(GroupTerm([Literal('x')]))

    def test_validity(self):
        inequation = LGroupInequation(Atom(GroupTerm([])), self.x.join(self.x.inv()))
        self.assertTrue(inequation.is_valid())
        inequation = LGroupInequation(Atom(GroupTerm([])), self.x)
        self.assertFalse(inequation.is_valid())

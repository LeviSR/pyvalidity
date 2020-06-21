from unittest import TestCase

from GroupTerm import GroupTerm
from LGroupInequation import LGroupInequation
from LGroupTerm import Atom
from Literal import Literal


class TestLGroupInequation(TestCase):
    def setUp(self):
        self.x = Atom(GroupTerm([Literal('x')]))

    def test_validity(self):
        inequation = LGroupInequation(Atom(GroupTerm([])), self.x.join(self.x.inv()))
        self.assertTrue(inequation.is_valid())

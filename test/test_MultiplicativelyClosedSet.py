from unittest import TestCase
import unittest

from Literal import Literal
from GroupTerm import GroupTerm
from MultiplicativelyClosedSet import MultiplicativelyClosedSet


class TestMultiplicativelyClosedSet(TestCase):
    def setUp(self):
        self.terms = {GroupTerm([Literal('x')]), GroupTerm([Literal('y')])}

    def test_close(self):
        closed = MultiplicativelyClosedSet(self.terms, 2)
        self.assertEqual(6, len(closed), closed.__str__() +
                         " isn't the closure of {x, y} ...")

    def test_trust(self):
        closed = MultiplicativelyClosedSet(self.terms, 2, True)
        self.assertEqual(2, len(closed),
                         "the True in the __init__ does nothing")


if __name__ == '__main__':
    unittest.main()

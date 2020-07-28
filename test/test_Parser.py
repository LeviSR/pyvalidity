from unittest import TestCase

from GroupTerm import GroupTerm
from LGroupTerm import Atom
from Literal import Literal
from Parser import Parser


class TestParser(TestCase):
    def setUp(self) -> None:
        self.parser = Parser("(x)")
        self.x = Atom(GroupTerm([Literal('x')]))
        self.y = Atom(GroupTerm([Literal('y')]))
        self.z = Atom(GroupTerm([Literal('z')]))
        self.xyz = self.x.prod(self.y).prod(self.z)
        self.e = Atom(GroupTerm([]))

    def test_strip(self):
        self.assertEqual(self.parser.string, "x")

    def test_atom(self):
        self.assertEqual(self.xyz, Parser("xyz").parse())
        self.assertEqual(self.e, Parser("e "). parse())
        self.assertNotEqual(Parser("x").parse(), Parser("X").parse())

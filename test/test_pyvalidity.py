from unittest import TestCase

from pyvalidity.Parser import Parser


class TestSantschisEquations(TestCase):
    def _check_valid(self, string):
        self.assertTrue(Parser(string).parse().is_valid())

    def _check_invalid(self, string):
        self.assertFalse(Parser(string).parse().is_valid())

    def test_distributive(self):
        self._check_valid( "x ^ (y v z) = (x ^ y) v (x ^ z) ")

    def test_mul_distributive1(self):
        self._check_valid("x(y v z)w = xyw v xzw")

    def test_mul_distributive2(self):
        self._check_valid("x(y ^ z)w = xyw ^ xzw ")

    def test_de_morgan1(self):
        self._check_valid("X ^ Y = -(x v y)")

    def test_de_morgan2(self):
        self._check_valid("X v Y = -(x ^ y)")

    # in Georges book
    def test_exercise18(self):
        self._check_valid("e <= x v X")
        self._check_valid("xy ^ e <= x v y")

    # in Almudenas thesis
    def test_example_1point3point6(self):
        self._check_valid("e <= xx v yy v XY")

    def test_left_prelinearity(self):
        self._check_valid("(Xy ^ e) v (Yx ^ e) = e")

    def test_right_prelinearity(self):
        self._check_valid("(xY ^ e) v (yX ^ e) = e")

    def test_commutativity(self):
        self._check_invalid("xy = yx")

    def test_example_1point3point7(self):
        self._check_invalid("e <= xx v xy v yX ")

    def test_representable_l_groups(self):
        self._check_invalid("e <= x v yXY")

    def test_weakly_abelian(self):
        self._check_invalid("(x ^ e)(x ^ e) <= Y(x ^ e)y")

    def test_representable_l_monoids(self):
        # hard, can take more than a minute. comment this out if you're just checking functionality
        pass
        self._check_invalid("xyz ^ rst <= xsz v ryt")

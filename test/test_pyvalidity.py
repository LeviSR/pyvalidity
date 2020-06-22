from unittest import TestCase

from pyvalidity.Parser import Parser


class TestSantschisEquations(TestCase):
    def setUp(self) -> None:
        self.valid_strings = [
            "x ^ (y v z) = (x ^ y) v (x ^ z) ",
            "x(y v z)w = xyw v xzw",
            "x(y ^ z)w = xyw ^ xzw ",
            "X ^ Y = -(x v y)",
            "X v Y = -(x ^ y)",
            "e <= x v X",
            "xy ^ e <= x v y",
            "e <= xx v yy v XY",
            "(Xy ^ e) v (Yx ^ e) = e",
            "(xY ^ e) v (yX ^ e) = e"
        ]

        self.invalid_strings = [
             "e <= xx v xy v yX ",
             "(x ^ e)(x ^ e) <= Y(x ^ e)y",         # this one is hard apparently, but doable.
                                                    # expect it to take 1-5 seconds. it is not
                                                    # consistent how long it takes.
             "e <= x v (yXY)",
             # "(xyz) ^ (rst) <= (xsz) v (ryt)"      # very hard.
        ]

    def test_valids(self):
        for s in self.valid_strings:
            self.assertTrue(Parser(s).parse().is_valid())

    def test_invalids(self):
        for s in self.invalid_strings:
            self.assertFalse(Parser(s).parse().is_valid())

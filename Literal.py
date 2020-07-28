class Literal:

    def __init__(self, char: chr, is_inverted: bool = False):
        if char == '':
            assert False
        self.char = char
        self.is_inverted = is_inverted

    def __str__(self):
        if self.is_inverted:
            return self.char.upper()
        return self.char

    def __eq__(self, other):
        return self.char == other.char and self.is_inverted == other.is_inverted

    def inv(self):
        return Literal(self.char, not self.is_inverted)

    def __hash__(self):
        return str(self).__hash__()

    def non_inverted(self):
        return Literal(self.char)

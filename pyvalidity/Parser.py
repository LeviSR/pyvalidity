

# a string representing a formula is made up of random characters encoding variables,
# which are not allowed to be '^', 'v', '-', '(', ')', 'e'
from GroupTerm import GroupTerm
from LGroupEquation import LGroupEquation
from LGroupInequation import LGroupInequation
from LGroupTerm import Atom, LGroupTerm, Meet, Join, Prod
from Literal import Literal



class Parser:
    meet_delimiter = '^'
    join_delimiter = 'v'
    inv_character = '-'

    def __init__(self, string: str):
        assert brackets_match(string)
        self.string = string[:]
        self.string = self.string.replace(" ", "")
        assert ' ' not in self.string
        self.strip_unnecessary_outer_brackets()

    def strip_unnecessary_outer_brackets(self):
        # unnecessary if it's outside and has only one "bracket component"
        if self.string[0] == '(' and self.string[-1] == ')' and components(self.string) == 1:
            self.string = self.string[1:-1]
            self.strip_unnecessary_outer_brackets()

    def is_atom(self):
        if self.is_inequation() or self.is_equation():
            return False

        # the string is an atom if there are no '^', 'v' and '-' and brackets
        return self.meet_delimiter not in self.string \
            and self.join_delimiter not in self.string \
            and self.inv_character not in self.string \
            and '(' not in self.string \
            and ')' not in self.string

    def parse_atom(self) -> Atom:
        assert self.meet_delimiter not in self.string
        assert self.join_delimiter not in self.string
        assert self.inv_character not in self.string
        literals = []
        for char in self.string:
            if char.lower() == 'e':
                pass
            elif char.isupper():
                literals.append(Literal(char.lower(), True))
            else:
                literals.append(Literal(char))
        return Atom(GroupTerm(literals))

    def is_inverse(self):
        if self.is_inequation() or self.is_equation():
            return False
        return self.string[0] == '-' \
            and (len(self.string) == 2
                 or (self.string[1] == '('
                     and self.string[-1] == ')'))

    def parse_inverse(self) -> LGroupTerm:
        new_parser = Parser(self.string[1:])
        return new_parser.parse().inv()

    def is_meet(self):
        if self.is_inequation() or self.is_equation():
            return False
        working_string = replace_brackets_by_nothing(self.string)
        return self.meet_delimiter in working_string

    def parse_meet(self):
        meetand_strings = []
        current_string = ''
        stack_height = 0
        for c in self.string:
            if c != self.meet_delimiter:
                current_string += c
            if c == '(':
                stack_height += 1
            if c == ')':
                stack_height -= 1
            if stack_height == 0 and c == self.meet_delimiter:
                meetand_strings.append(current_string)
                current_string = ''
        meetand_strings.append(current_string)
        return Meet({Parser(s).parse() for s in meetand_strings})

    def is_join(self):
        if self.is_inequation() or self.is_equation():
            return False
        working_string = replace_brackets_by_nothing(self.string)
        return self.join_delimiter in working_string

    def parse_join(self):
        joinand_strings = []
        current_string = ''
        stack_height = 0
        for c in self.string:
            if c != self.join_delimiter:
                current_string += c
            if c == '(':
                stack_height += 1
            if c == ')':
                stack_height -= 1
            if stack_height == 0 and c == self.join_delimiter:
                joinand_strings.append(current_string)
                current_string = ''
        joinand_strings.append(current_string)
        return Join({Parser(s).parse() for s in joinand_strings})

    def parse_prod(self):
        factor_strings = []
        stack_height = 0
        current_string = ''
        for c in self.string:
            current_string += c
            if c == '(':
                stack_height += 1
            if c == ')':
                stack_height -= 1
            if stack_height == 0:
                assert c not in {self.meet_delimiter, self.join_delimiter, self.inv_character}
                factor_strings.append(current_string)
                current_string = ''
        assert len(factor_strings) > 1
        return Prod([Parser(s).parse() for s in factor_strings])

    def is_inequation(self):
        return '<=' in self.string

    def parse_inequation(self):
        sides = self.string.split('<=')
        return LGroupInequation(Parser(sides[0]).parse(), Parser(sides[1]).parse())

    def is_equation(self):
        return not self.is_inequation() and '=' in self.string

    def parse_equation(self):
        sides = self.string.split('=')
        return LGroupEquation(Parser(sides[0]).parse(), Parser(sides[1]).parse())

    def parse(self):
        if self.is_atom():
            return self.parse_atom()
        if self.is_inverse():
            return self.parse_inverse()
        if self.is_meet():
            return self.parse_meet()
        if self.is_join():
            return self.parse_join()
        if self.is_inequation():
            return self.parse_inequation()
        if self.is_equation():
            return self.parse_equation()

        # this one is sort of hard to check, so it's the default
        return self.parse_prod()

    def __str__(self):
        return "Parser of " + self.string


def replace_brackets_by_nothing(string: str) -> str:
    stack_height = 0
    new_string = ''
    for c in string:
        if c == '(':
            stack_height += 1
        elif c == ')':
            stack_height -= 1
        elif stack_height == 0:
            new_string += c
    return new_string


def brackets_match(string) -> bool:
    stack_height = 0
    for c in string:
        if c == '(':
            stack_height += 1
        elif c == ')':
            stack_height -= 1
        if stack_height < 0:
            return False
    return stack_height == 0


def components(string):
    stack_height = 0
    comps = 0
    for c in string:
        if c == '(':
            stack_height += 1
        elif c == ')':
            stack_height -= 1
            if stack_height == 0:
                comps += 1
    return comps



# a string representing a formula is made up of random characters encoding variables,
# which are not allowed to be '^', 'v', '-', '(', ')', 'e'
from GroupTerm import GroupTerm
from LGroupTerm import Atom, LGroupTerm, Meet, Join, Prod
from Literal import Literal


class Parser:
    meet_delimiter = '^'
    join_delimiter = 'v'
    inv_character = '-'

    def __init__(self, string: str):
        self.string = string[:]
        self.string.replace(" ", "")
        self.strip_unnecessary_outer_brackets()

    def strip_unnecessary_outer_brackets(self):
        if self.string[0] == '(' and self.string[-1] == ')':
            self.string = self.string[1:-1]

    def is_atom(self):
        # the string is an atom if there are no '^', 'v' and '-' and brackets
        return self.meet_delimiter not in self.string \
           and self.join_delimiter not in self.string \
           and self.inv_character not in self.string \
           and '(' not in self.string \
           and ')' not in self.string

    def parse_atom(self) -> Atom:
        literals = []
        for char in self.string:
            if char.isupper():
                literals.append(Literal(char.lower(), True))
            else:
                literals.append(Literal(char))
        return Atom(GroupTerm(literals))

    def is_inverse(self):
        return self.string[-1] == '-' \
               and (len(self.string) == 2
                    or (self.string[0] == '('
                        and self.string[-1] == ')'))

    def parse_inverse(self) -> LGroupTerm:
        new_parser = Parser(self.string[:-1])
        return new_parser.parse().inv()

    def is_meet(self):
        working_string = replace_brackets_by_nothing(self.string)
        return self.meet_delimiter in working_string

    def parse_meet(self):
        meetand_strings = self.string.split(self.meet_delimiter)
        return Meet({Parser(s).parse() for s in meetand_strings})

    def is_join(self):
        working_string = replace_brackets_by_nothing(self.string)
        return self.join_delimiter in working_string

    def parse_join(self):
        joinand_strings = self.string.split(self.meet_delimiter)
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
                factor_strings.append(current_string)
                current_string = ''
        return Prod([Parser(s).parse() for s in factor_strings])

    def parse(self) -> LGroupTerm:
        if self.is_atom():
            return self.parse_atom()
        if self.is_inverse():
            return self.parse_inverse()
        if self.is_meet():
            return self.parse_meet()
        if self.is_join():
            return self.parse_join()
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

from typing import List, Set

from pyvalidity.Literal import Literal


class GroupTerm:
    # We make the convention that all group terms are always reduced.
    def __init__(self, literals: List[Literal]):
        self.literals = literals
        self.reduce()

    def __eq__(self, other):
        # assert self.is_reduced() and other.is_reduced()
        return isinstance(other, GroupTerm) and self.literals == other.literals

    def __str__(self):
        if self.literals == []:
            return 'e'
        string = ""
        for lit in self.literals:
            string = string + lit.__str__()
        return string

    def __hash__(self):
        return self.__str__().__hash__()

    def __len__(self):
        return self.literals.__len__()

    def reduce(self):
        i = 0
        while i <= len(self.literals) - 2:
            if self.literals[i] == self.literals[i+1].inv():
                del self.literals[i:i+2]
            else:
                i = i + 1

    def times(self, other):
        return GroupTerm(self.literals + other.literals)

    def inv(self):
        return GroupTerm([x.inv() for x in self.literals][::-1])

    def is_reduced(self) -> bool:
        for i in range(len(self.literals) - 1):
            if self.literals[i] == self.literals[i+1].inv():
                return False
        return True

    def positive_literals(self) -> Set[Literal]:
        result = set()
        for x in self.literals:
            if x.is_inverted:
                result.add(x.inv())
            else:
                result.add(x)
        return result

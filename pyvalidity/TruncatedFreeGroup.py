from pyvalidity.Literal import Literal
from pyvalidity.GroupTerm import GroupTerm
from typing import Set


class TruncatedFreeGroup:
    def __init__(self, max_length: int, generators: Set[Literal]):
        self.max_length = max_length
        self.generators = generators
        self.elements = set()
        if max_length >= 0:
            self.elements.add(GroupTerm([]))
        if max_length >= 1:
            self.elements |= {GroupTerm([x]) for x in generators} \
                           | {GroupTerm([x.inv()]) for x in generators}
        if max_length >= 2:
            shorter_elements = TruncatedFreeGroup(max_length - 1,
                                                  generators).elements
            self.elements = shorter_elements \
                | {GroupTerm([x]).times(t) for x in generators for t in shorter_elements} \
                | {t.times(GroupTerm([x])) for x in generators for t in shorter_elements} \
                | {t.times(GroupTerm([x.inv()])) for x in generators for t in shorter_elements} \
                | {GroupTerm([x.inv()]).times(t) for x in generators for t in shorter_elements}

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return '{' + ', '.join([str(t) for t in self.elements]) + '}'

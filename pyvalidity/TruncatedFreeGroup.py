from pyvalidity.Literal import Literal
from pyvalidity.GroupTerm import GroupTerm
from typing import Set


# has about 2 000 000 elements for max_length = 6 and 6 generators. Takes ages to compute, too.
class TruncatedFreeGroup:
    stored = []

    def __init__(self, max_length: int, generators: Set[Literal]):
        self.max_length = max_length
        self.generators = generators
        self.elements = set()
        copied = False
        for group in TruncatedFreeGroup.stored:
            if len(self.generators) == len(group.generators) and self.max_length == group.max_length:
                self.replace_generators_and_add(group)
                copied = True
                break
        if not copied:
            self.construct()
            TruncatedFreeGroup.stored.append(self)

    def replace_generators_and_add(self, group):
        for element in group.elements:
            self.elements.add(element.replace_under_bijection(list(group.generators),
                                                              list(self.generators)))

    def construct(self):
        if self.max_length >= 0:
            self.elements.add(GroupTerm([]))
        if self.max_length >= 1:
            self.elements |= {GroupTerm([x]) for x in self.generators} \
                           | {GroupTerm([x.inv()]) for x in self.generators}
        if self.max_length >= 2:
            shorter_elements = TruncatedFreeGroup(self.max_length - 1,
                                                  self.generators).elements
            # seems to break down when shorter_elements has more than 100 000 elements.
            self.elements = shorter_elements \
                | {GroupTerm([x]).times(t) for x in self.generators for t in shorter_elements} \
                | {t.times(GroupTerm([x])) for x in self.generators for t in shorter_elements} \
                | {t.times(GroupTerm([x.inv()])) for x in self.generators for t in shorter_elements} \
                | {GroupTerm([x.inv()]).times(t) for x in self.generators for t in shorter_elements}

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return '{' + ', '.join([str(t) for t in self.elements]) + '}'

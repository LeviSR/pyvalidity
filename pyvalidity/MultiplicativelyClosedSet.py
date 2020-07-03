from typing import Set, List

from Literal import Literal
from pyvalidity.GroupTerm import GroupTerm

import itertools


# The name of this class should probably be "Truncated
# Multiplicatively Closed Set".
class MultiplicativelyClosedSet:
    elements: Set[GroupTerm]
    max_length: int
    generators: List[Literal]

    # The parameter is_already_closed bypasses the closure procedure, which
    # can make initialisation more efficient in case the input set is already
    # known to be multiplicatively closed.
    def __init__(self,
                 some_set: Set[GroupTerm],
                 max_length: int,
                 is_already_closed=False,
                 generators=None):
        self.max_length = max_length
        self.elements = some_set.copy()

        # finding generators
        if generators is None:
            self.generators = set()
            for x in self.elements:
                self.generators |= set(map(Literal.non_inverted, x.literals))
            self.generators = list(self.generators)

        # closing
        if is_already_closed:
            self.unchecked_pairs = []
        else:
            self.unchecked_pairs = itertools.product(self.elements, repeat=2)
            self.close()
        assert self.unchecked_pairs == []

    # TODO properly test and clean up
    def close(self):
        add_later_to_new_elements = {s.times(t) for s, t in self.unchecked_pairs
                                     if len(s.times(t)) <= self.max_length
                                     and s.times(t) not in self.elements}
        self.unchecked_pairs = []
        found_something = True


        while found_something:
            found_something = False
            new_elements = add_later_to_new_elements
            add_later_to_new_elements = set()
            self.elements |= new_elements

            # are of length <= 2 for max_length = 3, which is good enough
            short_elements = [t for t in self.elements if len(t) < self.max_length]
            long_elements = [t for t in self.elements if len(t) == self.max_length]

            # the concatenation of left is long_elements, and looks like
            # [[things that start with gen0], [things that start with gen0^-1], [things that start with gen1], ...]
            left = [[] for _ in range(2 * len(self.generators))]
            right = [[] for _ in range(2 * len(self.generators))]
            for t in long_elements:
                if t != GroupTerm([]):
                    assert t.literals[0].non_inverted() in self.generators \
                           and t.literals[-1].non_inverted() in self.generators
                    for i, gen in enumerate(self.generators):
                        assert not gen.is_inverted
                        if t.literals[0].non_inverted() == gen:
                            left_index = 2 * i + (1 if t.literals[0].is_inverted else 0)
                        if t.literals[-1].non_inverted() == gen:
                            right_index = 2 * i + (1 if t.literals[-1].is_inverted else 0)
                    left[left_index].append(t)
                    right[right_index].append(t)

            for s in new_elements:
                if len(s) == self.max_length:
                    for i, gen in enumerate(self.generators):
                        if s.literals[0].non_inverted() == gen:
                            left_index = 2 * i + (0 if s.literals[0].is_inverted else 1)
                        if s.literals[-1].non_inverted() == gen:
                            right_index = 2 * i + (0 if s.literals[-1].is_inverted else 1)
                    for t in left[right_index]:
                        p = s.times(t)
                        if len(p) <= self.max_length and p not in self.elements:
                            add_later_to_new_elements.add(p)
                            found_something = True
                    for t in right[left_index]:
                        p = t.times(s)
                        if len(p) <= self.max_length and p not in self.elements:
                            add_later_to_new_elements.add(p)
                            found_something = True
                    for t in short_elements:
                        for p in [t.times(s), s.times(t)]:
                            if len(p) <= self.max_length and p not in self.elements:
                                add_later_to_new_elements.add(p)
                                found_something = True
                else:
                    for t in self.elements:
                        for p in [t.times(s), s.times(t)]:
                            if len(p) <= self.max_length and p not in self.elements:
                                add_later_to_new_elements.add(p)
                                found_something = True
            pass
        pass

    def add(self, element: GroupTerm):
        assert self.unchecked_pairs == []
        assert element.__len__() <= self.max_length
        for lit in element.literals:
            if lit.non_inverted() not in self.generators:
                self.generators.append(lit.non_inverted())
        self.unchecked_pairs = [(element, t) for t in self.elements] \
                               + [(t, element) for t in self.elements] \
                               + [(element, element)]
        self.elements.add(element)
        self.close()

    def __len__(self):
        return self.elements.__len__()

    def __str__(self):
        return '{' + ', '.join([str(t) for t in self.elements]) + '}'

from typing import Set
from pyvalidity.GroupTerm import GroupTerm

import itertools


# The name of this class should probably be "Truncated
# Multiplicatively Closed Set".
class MultiplicativelyClosedSet:
    elements: Set[GroupTerm]
    max_length: int

    # The parameter is_already_closed bypasses the closure procedure, which
    # can make initialisation more efficient in case the input set is already
    # known to be multiplicatively closed.
    def __init__(self,
                 some_set: Set[GroupTerm],
                 max_length: int,
                 is_already_closed=False):
        self.max_length = max_length
        self.elements = some_set.copy()

        if is_already_closed:
            self.unchecked_pairs = []
        else:
            self.unchecked_pairs = itertools.product(self.elements, repeat=2)
            self.close()
        assert self.unchecked_pairs == []

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
            for s in new_elements:
                for t in self.elements:
                    products = [s.times(t), t.times(s)]
                    for p in products:
                        if len(p) <= self.max_length and p not in self.elements:
                            add_later_to_new_elements.add(p)
                            found_something = True
            pass
        pass

    def add(self, element: GroupTerm):
        assert self.unchecked_pairs == []
        assert element.__len__() <= self.max_length
        self.unchecked_pairs = [(element, t) for t in self.elements] \
            + [(t, element) for t in self.elements] \
            + [(element, element)]
        self.elements.add(element)
        self.close()

    def __len__(self):
        return self.elements.__len__()

    def __str__(self):
        return '{' + ', '.join([str(t) for t in self.elements]) + '}'

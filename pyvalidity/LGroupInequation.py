from typing import Set, List

from pyvalidity.MultiplicativelyClosedSet import MultiplicativelyClosedSet
from pyvalidity.PartialOrder import PartialOrder
from pyvalidity.TruncatedFreeGroup import TruncatedFreeGroup
from pyvalidity.LGroupTerm import LGroupTerm, Atom, Join


class LGroupInequation:
    # LGroupInequation(s, t) stands for s <= t
    def __init__(self, left_hand_side: LGroupTerm, right_hand_side: LGroupTerm):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side

    # LGroupInequation(s, t) returns ts^{-1}, which is the thing that "should be positive"
    def _relevant_cnf(self) -> LGroupTerm:
        return self.right_hand_side.prod(self.left_hand_side.inv()).cnf()

    def is_valid(self) -> bool:
        good_cnf = self._relevant_cnf().cnf3()
        cnf_set = _cnf_to_set(good_cnf)
        for candidate in cnf_set:
            max_length = max([len(elem) for elem in candidate])
            candidate_terms = {t.atom for t in candidate}
            closed = MultiplicativelyClosedSet(candidate_terms, max_length)
            generators = set()
            for x in candidate_terms:
                generators |= x.positive_literals()
            truncated = TruncatedFreeGroup(max_length, generators)
            partial = PartialOrder(closed, truncated)
            if partial.extends_to_total_order():
                return False
        # none of the meetands extend
        return True

    def __str__(self):
        return str(self.left_hand_side) + " <= " + str(self.right_hand_side)


def _cnf_to_set(cnf: LGroupTerm) -> List[Set[LGroupTerm]]:
    # cnf is now of one of the following forms:
    # (i)   a meet of joins of atoms
    # (ii)  a join of atoms
    # (iii) an atom

    # (i)
    if cnf.is_atom():
        return [{cnf}]
    if cnf.is_join():
        return [cnf.joinands]
    return [t.joinands for t in cnf.meetands]

from pyvalidity.MultiplicativelyClosedSet import MultiplicativelyClosedSet
from pyvalidity.TruncatedFreeGroup import TruncatedFreeGroup
from pyvalidity.GroupTerm import GroupTerm


class PartialOrder:
    def __init__(self,
                 positives: MultiplicativelyClosedSet,
                 truncated_group: TruncatedFreeGroup,
                 complement=None):
        assert positives.max_length == truncated_group.max_length
        self.max_length = positives.max_length
        self.positives = positives.elements
        self.truncated_group = truncated_group

        if complement is None:
            self.complement = truncated_group.elements.copy()
            self.complement -= self.positives
            if GroupTerm([]) in self.complement:
                self.complement.remove(GroupTerm([]))
        else:
            self.complement = complement
        assert GroupTerm([]) not in self.complement

    def extends_to_total_order(self):
        if GroupTerm([]) in self.positives:
            return False
        assert GroupTerm([]) not in self.complement
        if all(t in self.positives or t.inv() in self.positives
               for t in self.complement):
            return True
        # now there exists t in ambient_set such that neither
        # t nor t^{-1} are in positives.
        assert self.complement != set()

        # should be equivalent to:
        # candidates = [t for t in self.complement if t not in self.positives and t.inv() not in self.positives]
        # t = min(candidates, key=len)for t in self.complement:

        started = False
        for t in self.complement:
            if not started:
                best_t = t
                started = True
            if len(t) <= 2:
                best_t = t
                break
            if len(t) <= len(best_t):
                best_t = t
        t = best_t
        # t is now a candidate to extend with.
        assert t not in self.positives and t.inv() not in self.positives
        for s in [t, t.inv()]:
            new_set = MultiplicativelyClosedSet(self.positives.copy(),
                                                self.max_length,
                                                True)
            new_set.add(s)
            new_complement = self.complement.copy()
            new_complement.remove(s)
            child = PartialOrder(new_set, self.truncated_group, new_complement)
            if child.extends_to_total_order():
                return True
        return False

    def __str__(self):
        return '{' + ', '.join([str(t) for t in self.positives]) + '}'

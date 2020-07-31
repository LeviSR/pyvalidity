from MultiplicativelyClosedSet import MultiplicativelyClosedSet
from TruncatedFreeGroup import TruncatedFreeGroup
from GroupTerm import GroupTerm


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
            if self.max_length >= 1:
                short = truncated_group.one_shorter().elements.copy()
                self.complement = short
            else:
                self.complement = truncated_group.elements.copy()
            self.complement -= self.positives | {x.inv() for x in self.positives}
            if GroupTerm([]) in self.complement:
                self.complement.remove(GroupTerm([]))
        else:
            self.complement = complement
        assert GroupTerm([]) not in self.complement

    def extends_to_total_order(self, depth):
        print("The depth is", depth)
        if GroupTerm([]) in self.positives:
            return False
        assert GroupTerm([]) not in self.complement
        if not self.complement:
            return True
        # now there exists t in ambient_set such that neither
        # t nor t^{-1} are in positives.
        assert self.complement != set()

        t = min(self.complement, key=len)

        # t is now a candidate to extend with.
        assert t not in self.positives and t.inv() not in self.positives
        for s in [t, t.inv()]:
            new_set = MultiplicativelyClosedSet(self.positives.copy(),
                                                self.max_length,
                                                True)
            new_set.add(s)
            new_complement = self.complement.copy()
            new_complement -= new_set.elements | {x.inv() for x in new_set.elements}
            child = PartialOrder(new_set, self.truncated_group, new_complement)
            if child.extends_to_total_order(depth+1):
                return True
        return False

    def __str__(self):
        return '{' + ', '.join([str(t) for t in self.positives]) + '}'

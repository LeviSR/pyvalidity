from pyvalidity.LGroupTerm import LGroupTerm


class LGroupInequation:
    # LGroupInequation(s, t) stands for s <= t
    def __init__(self, left_hand_side: LGroupTerm, right_hand_side: LGroupTerm):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side

    # LGroupInequation(s, t) returns ts^{-1}, which is the thing that "should be positive"
    def _relevant_term(self) -> LGroupTerm:
        return self.right_hand_side.prod(self.left_hand_side.inv())

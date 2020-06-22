from pyvalidity.LGroupInequation import LGroupInequation
from pyvalidity.LGroupTerm import LGroupTerm


class LGroupEquation:
    def __init__(self, left_hand_side: LGroupTerm, right_hand_side: LGroupTerm):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side

    def is_valid(self):
        return LGroupInequation(self.left_hand_side, self.right_hand_side).is_valid() \
            and LGroupInequation(self.right_hand_side, self.left_hand_side).is_valid()

    def __str__(self):
        return str(self.left_hand_side) + " = " + str(self.right_hand_side)

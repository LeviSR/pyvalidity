from typing import Set, List

from pyvalidity.GroupTerm import GroupTerm


# is either an atom, or a meet, join of a set of terms, or a product of a list
# of terms. In particular, meet, join, product are all associative, and meet,
# join satisfy the absorption law. Implements the cnf of an LGroupTerm
class LGroupTerm:
    def is_identity(self):
        pass

    # not sure if having the hash depend on the string representation will
    # cause a problem later on
    def __hash__(self):
        return self.__str__().__hash__()

    def meet(self, other):
        return Meet({self, other})

    def join(self, other):
        return Join({self, other})

    def prod(self, other):
        return Prod([self, other])

    def cast_to(self, other):
        self.__class__ = other.__class__
        if type(other) is Atom:
            self.atom = other.atom
        elif type(other) is Meet:
            self.meetands = other.meet
        elif type(other) is Join:
            self.joinands = other.join
        elif type(other) is Prod:
            self.factors = other.prod
        self.reduce()


class Atom(LGroupTerm):
    def __init__(self, atom: GroupTerm):
        self.atom = atom

    def __str__(self):
        return self.atom.__str__()

    def __eq__(self, other):
        return isinstance(other, Atom) and self.atom == other.atom

    __hash__ = LGroupTerm.__hash__

    def is_identity(self):
        return self.atom == GroupTerm([])

    def reduce(self):
        pass

    def cnf(self):
        return self

    def inv(self):
        return Atom(self.atom.inv())


class Meet(LGroupTerm):
    def __init__(self, meetands: Set[LGroupTerm]):
        self.meetands = meetands
        self.reduce()
        if len(meetands) == 1:
            for t in meetands:
                self.cast_to(t)

    def __str__(self):
        if len(self.meetands) == 0:
            return "(empty meet)"
        string = ""
        for t in self.meetands:
            string += t.__str__() + " ^ "
        return "(" + string[:-3] + ")"

    def __eq__(self, other):
        return isinstance(other, Meet) and self.meetands == other.meetands

    __hash__ = LGroupTerm.__hash__

    def is_identity(self):
        return False

    # assumes that meetands are reduced. absorbs meets
    def reduce(self):
        new_meetands = set()
        for t in self.meetands:
            if isinstance(t, Meet):
                new_meetands |= t.meetands
            else:
                new_meetands.add(t)
        self.meetands = new_meetands

    # cnf(s ^ t) = cnf(s) ^ cnf(t)
    def cnf(self):
        cnfs = set()
        for meetand in self.meetands:
            cnfs.add(meetand.cnf())
        return Meet(cnfs)

    def inv(self):
        return Join({x.inv() for x in self.meetands})


class Join(LGroupTerm):
    def __init__(self, joinands: Set[LGroupTerm]):
        if len(joinands) == 1:
            for t in joinands:
                self.cast_to(t)
        else:
            self.joinands = joinands
        self.reduce()

    def __str__(self):
        if len(self.joinands) == 0:
            return "empty join"
        string = ""
        for t in self.joinands:
            string += t.__str__() + " v "
        return "(" + string[:-3] + ")"

    def __eq__(self, other):
        return isinstance(other, Join) and self.joinands == other.joinands

    __hash__ = LGroupTerm.__hash__

    def is_identity(self):
        return False

    # absorbs joins. assumes that joinands are reduced
    def reduce(self):
        new_joinands = set()
        for t in self.joinands:
            if isinstance(t, Join):
                new_joinands |= t.joinands
            else:
                new_joinands.add(t)
        self.joinands = new_joinands

    # cnf((r ^ s) v t) = cnf(r v t) ^ cnf(s v t)
    # otherwise cnf(s v t) = cnf(s) v cnf(t)
    def cnf(self):
        has_meets = False
        for rs in self.joinands:
            if isinstance(rs, Meet):
                has_meets = True
                break

        # rs is now the first meet
        if has_meets:
            rest = set()
            for ss in self.joinands:
                if ss != rs:
                    rest.add(ss)

            # rest should be nonempty
            assert rest != set()

            new_meetands = set()
            for r in rs.meetands:
                new_meetands.add(r.join(Join(rest)).cnf())

            return Meet(new_meetands)

        cnfs = set()
        for joinand in self.joinands:
            cnfs.add(joinand.cnf())
        return Join(cnfs)

    def inv(self):
        return Meet({x.inv() for x in self.joinands})


class Prod(LGroupTerm):
    def __init__(self, factors: List[LGroupTerm]):
        if len(factors) == 1:
            for t in factors:
                self.cast_to(t)
        else:
            self.factors = factors
        self.reduce()

    def __str__(self):
        if len(self.factors) == 0:
            return "e"

        string = ""
        for t in self.factors:
            string += t.__str__()

        return string

    def is_identity(self):
        return self.factors == []

    # removes identities. assumes that components are reduced
    def reduce(self):
        new_factors = []
        for factor in self.factors:
            if not factor.is_identity():
                new_factors.append(factor)

        self.factors = new_factors

    def cnf(self):
        has_meets = False
        for rs in self.factors:
            if isinstance(rs, Meet):
                has_meets = True
                rs_index = self.factors.index(rs)
                break

        # rs is now the first meet
        if has_meets:
            rest_left = []
            rest_right = []
            for i, factor in enumerate(self.factors):
                if i < rs_index:
                    rest_left.append(factor)
                elif i > rs_index:
                    rest_right.append(factor)

            new_meetands = set()
            for r in rs.meetands:
                new_meetands.add(Prod(rest_left)
                                 .prod(r)
                                 .prod(Prod(rest_right))
                                 .cnf())
            return Meet(new_meetands)

        has_joins = False
        for rs in self.factors:
            if isinstance(rs, Join):
                has_joins = True
                rs_index = self.factors.index(rs)
                break

        # rs is now the first join
        if has_joins:
            rest_left = []
            rest_right = []
            for i, factor in enumerate(self.factors):
                if i < rs_index:
                    rest_left.append(factor)
                elif i > rs_index:
                    rest_right.append(factor)

            new_joinands = set()
            for r in rs.joinands:
                new_joinands.add(Prod(rest_left)
                                 .prod(r)
                                 .prod(Prod(rest_right))
                                 .cnf())
            return Join(new_joinands)

        # if it's here there's neither meets nor joins in the factors
        cnfs = []
        for factor in self.factors:
            cnfs.append(factor.cnf())
        return Prod(cnfs)

    def inv(self):
        # list[::-1] is list reversed
        return Prod([x.inv() for x in self.factors][::-1])

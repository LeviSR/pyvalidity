from __future__ import annotations
from typing import Set, List, Any

from Literal import Literal
from pyvalidity.GroupTerm import GroupTerm


# is either an atom, or a meet, join of a set of terms, or a product of a list
# of terms. In particular, meet, join, product are all associative, and meet,
# join satisfy the absorption law. Implements the cnf of an LGroupTerm
class LGroupTerm:
    def is_identity(self) -> bool:
        pass

    # not sure if having the hash depend on the string representation will
    # cause a problem later on
    def __hash__(self):
        return self.__str__().__hash__()

    def meet(self, other) -> Meet:
        return Meet({self, other})

    def join(self, other) -> Join:
        return Join({self, other})

    def prod(self, other) -> Prod:
        return Prod([self, other])

    def cast_to(self, other) -> None:
        self.__class__ = other.__class__
        if other.is_atom():
            other: Atom
            self: Atom
            self.__init__(other.atom)
        elif other.is_meet():
            other: Meet
            self: Meet
            self.__init__(other.meetands)
        elif other.is_join():
            other: Join
            self: Join
            self.__init__(other.joinands)
        elif other.is_prod():
            other: Prod
            self: Prod
            self.__init__(other.factors)
        self.reduce()

    def is_atom(self) -> bool:
        return isinstance(self, Atom)

    def is_meet(self) -> bool:
        return isinstance(self, Meet)

    def is_join(self) -> bool:
        return isinstance(self, Join)

    def is_prod(self) -> bool:
        return isinstance(self, Prod)

    def inv(self) -> LGroupTerm:
        # this should not be executed here but in one of the subclasses
        pass

    def reduce(self) -> LGroupTerm:
        pass

    def cnf(self) -> LGroupTerm:
        pass

    # eliminates long atoms by replacing them with joins of shorter atoms, partially
    # made up of new literals (i.e., not currently appearing in )
    def cnf3(self) -> LGroupTerm:
        normal_cnf: LGroupTerm
        normal_cnf = self.cnf()
        if normal_cnf.is_atom():
            normal_cnf: Atom
            return _split_atom(normal_cnf, _Counter())
        elif normal_cnf.is_join():
            normal_cnf: Join
            if len(normal_cnf.joinands) <= 2:
                return normal_cnf
            counter = _Counter()
            new_joinands = set()
            for joinand in normal_cnf.joinands:
                joinand: Atom
                new_joinands.add(_split_atom(joinand, counter))
            return Join(new_joinands)
        # normal_cnf is now a meet
        assert normal_cnf.is_meet()
        normal_cnf: Meet
        return Meet({meetand.cnf3() for meetand in normal_cnf.meetands})


# abcdef |-> ab(-x0) v (x0)c(-x1) v (x1)d(-x2) v (x2)ef
# may cause problems if some variables are called x1 or something.
# but users are instructed to use single characters
def _split_atom(atom, counter) -> Join:
    if len(atom) <= 3:
        return atom
    first_literals = atom.atom.literals[:2] + [Literal('x0', False)]
    last_literals = [Literal('x' + str(len(atom) - 4), True)] + atom.atom.literals[-2:]
    first_meetand = Atom(GroupTerm(first_literals))
    last_meetand = Atom(GroupTerm(last_literals))

    joinands = {first_meetand, last_meetand}

    for mid in atom.atom.literals[2:-2]:
        pre = Literal('x' + str(counter.current), True)
        post = Literal('x' + str(counter.step()), False)
        joinands.add(Atom(GroupTerm([pre, mid, post])))

    return Join(joinands)


# helper class
class _Counter:
    current: int

    def __init__(self):
        self.current = 0

    def step(self):
        self.current += 1
        return self.current


class Atom(LGroupTerm):
    def __init__(self, atom: GroupTerm):
        self.atom = atom
        self.reduce()

    def __str__(self):
        return self.atom.__str__()

    def __eq__(self, other):
        return type(other) is Atom and self.atom == other.atom

    def __len__(self) -> str:
        return self.atom.__len__()

    __hash__ = LGroupTerm.__hash__

    def is_identity(self) -> bool:
        return self.atom == GroupTerm([])

    def reduce(self) -> None:
        assert self.atom.literals != ['']
        pass

    def cnf(self) -> LGroupTerm:
        return self

    def inv(self) -> LGroupTerm:
        return Atom(self.atom.inv())


class Meet(LGroupTerm):
    def __init__(self, meetands: Set[LGroupTerm]):
        self.meetands = meetands
        self.reduce()

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

    def is_identity(self) -> bool:
        return False

    # assumes that meetands are reduced. absorbs meets
    def reduce(self) -> None:
        new_meetands = set()
        for t in self.meetands:
            if isinstance(t, Meet):
                new_meetands |= t.meetands
            else:
                new_meetands.add(t)
        self.meetands = new_meetands

        if len(self.meetands) == 1:
            for t in self.meetands:
                self.cast_to(t)
                self.reduce()

    # cnf(s ^ t) = cnf(s) ^ cnf(t)
    def cnf(self) -> LGroupTerm:
        cnfs = set()
        for meetand in self.meetands:
            cnfs.add(meetand.cnf())
        return Meet(cnfs)

    def inv(self) -> LGroupTerm:
        return Join({x.inv() for x in self.meetands})


class Join(LGroupTerm):
    joinands: Set[LGroupTerm]

    def __init__(self, joinands: Set[LGroupTerm]):
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

    def is_identity(self) -> bool:
        return False

    # absorbs joins. assumes that joinands are reduced
    def reduce(self) -> None:
        new_joinands = set()
        for t in self.joinands:
            if isinstance(t, Join):
                new_joinands |= t.joinands
            else:
                new_joinands.add(t)
        self.joinands = new_joinands

        if len(self.joinands) == 1:
            for t in self.joinands:
                self.cast_to(t)
                self.reduce()

    # cnf((r ^ s) v t) = cnf(r v t) ^ cnf(s v t)
    # otherwise cnf(s v t) = cnf(s) v cnf(t)
    def cnf(self) -> LGroupTerm:
        has_meets = False

        rs = None
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
        self.factors = factors
        self.reduce()

    def __str__(self):
        if len(self.factors) == 0:
            return "e"

        string = ""
        for t in self.factors:
            string += t.__str__()

        return string

    def is_identity(self) -> bool:
        return self.factors == []

    # removes identities. assumes that components are reduced
    def reduce(self) -> None:
        new_factors = []
        # strip identities
        for factor in self.factors:
            if not factor.is_identity():
                new_factors.append(factor)
        self.factors = new_factors

        # absorb products
        i = 0
        while i < len(self.factors):
            if self.factors[i].is_prod():
                self.factors = self.factors[:i] + self.factors[i].factors + self.factors[i+1:]
            else:
                i += 1

        # multiply together consecutive factors that are atoms
        i = 0
        while i < len(self.factors) - 1:
            if self.factors[i].is_atom() and self.factors[i+1].is_atom():
                self.factors[i] = Atom(self.factors[i].atom.times(self.factors[i+1].atom))
                del self.factors[i+1]
            else:
                i += 1

        if len(self.factors) == 1:
            for t in self.factors:
                self.cast_to(t)
                self.reduce()

        if len(self.factors) == 0:
            self.cast_to(Atom(GroupTerm([])))

    def cnf(self) -> LGroupTerm:
        has_meets = False
        rs: Any
        rs = None
        rs_index = -1
        for rs in self.factors:
            if isinstance(rs, Meet):
                has_meets = True
                rs_index = self.factors.index(rs)
                break

        # rs is now the first meet
        rs: Meet
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
                new_meetand = Prod(rest_left).prod(r).prod(Prod(rest_right))
                new_meetands.add(new_meetand)
            return Meet(new_meetands)

        has_joins = False
        for rs in self.factors:
            if rs.is_join():
                has_joins = True
                rs_index = self.factors.index(rs)
                break

        # rs is now the first join
        rs: Join
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
                new_joinand = Prod(rest_left).prod(r).prod(Prod(rest_right)).cnf()
                new_joinands.add(new_joinand)
            return Join(new_joinands).cnf()

        # if it's here there's neither meets nor joins in the factors
        cnfs = []
        for factor in self.factors:
            cnfs.append(factor.cnf())
        return Prod(cnfs)

    def inv(self) -> Prod:
        # list[::-1] is list reversed
        return Prod([x.inv() for x in self.factors][::-1])

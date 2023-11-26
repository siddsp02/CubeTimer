# !usr/bin/env python3

from copy import copy
from itertools import batched
from typing import Iterator, NamedTuple, Self

MAX_ROTATIONS = 4


class Move(NamedTuple):
    value: str = ""

    def __str__(self) -> str:
        return str(self.value)

    def __add__(self, other: Self) -> Self | tuple[Self, Self]:
        if other == -self:
            return type(self)()
        if self.is_neutral:
            return other
        if other == self:
            return self * 2
        if other == self * 2:
            return -self
        return self, other

    __radd__ = __add__

    def __mul__(self, i: int) -> Self:
        i %= MAX_ROTATIONS
        if i == 0:
            return type(self)()
        if i == 1:
            return self
        if i % 2 == 0:
            return self.double()
        if i % 3 == 0:
            return -self
        return self

    __rmul__ = __mul__  # type: ignore

    def __neg__(self) -> Self:
        if self.value.endswith("2"):
            return self
        if self.value.endswith("'"):
            return type(self)(self.value[0])
        return type(self)(self.value + "'")

    def double(self) -> Self:
        if self.value.endswith("2"):
            return type(self)()
        if self.value.endswith("'"):
            return -self
        return type(self)(self.value + "2")

    @property
    def is_neutral(self) -> bool:
        return self == type(self)()

    @property
    def base(self) -> Self:
        if self.value.endswith(("'", "2")):
            return type(self)(self.value[0])
        return self

    def affected_by(self, other: Self) -> bool:
        if self.is_neutral or other.is_neutral:
            return False
        PAIRS = map(set, batched(map(Move, "LRUDFB"), 2))
        return {self.base, other.base} not in PAIRS


class MoveList:
    def __init__(self, moves: list[Move] | None = None) -> None:
        self.moves = moves if moves is not None else []

    def __str__(self) -> str:
        return " ".join(map(str, self))

    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, self.moves)

    def __add__(self, other: Self | Move) -> Self:
        ret = copy(self)
        if not isinstance(other, Move):
            raise NotImplementedError("To be implemented.")
        last_move = ret.moves.pop()
        last_move += other
        ret.moves += [last_move] if isinstance(last_move, Move) else last_move
        return ret

    def __iter__(self) -> Iterator[Move]:
        yield from self.moves


def main() -> None:
    L, R, U, D, F, B = map(Move, "LRUDFB")
    print(MoveList([L, R, -R, B, U, D, -D, U * 2, L * 3]))


if __name__ == "__main__":
    main()

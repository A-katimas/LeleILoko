from typing import Any, Iterator, cast, Iterable, Self


class Vector:
    CLASS_LEN: int = 0
    DIM_ORDER: str = "xyzabcdef"

    def __init__(
        self,
        *args: int
        | float
        | tuple[int | float, ...]
        | list[int | float]
        | list[int]
        | list[float]
        | None,
    ) -> None:
        if self.__iscompatible(args):
            self._dim_pos = tuple(cast(tuple[int | float, ...], args))
        elif len(args) == 1 and self.__iscompatible(args[0]):
            self._dim_pos = tuple(cast(Iterable[int | float], args[0]))
        else:
            raise ValueError(
                f"cant initialise {self.__class__.__name__} with {args}"
            )

    def __add__(self, other: Any) -> Self:
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] + a_b[1],
                        [(a, b) for a, b in zip(self, other)],
                    )
                )
            )
        raise TypeError(f"cant add {self} to {other}")

    def __sub__(self, other: Any) -> Self:
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] - a_b[1],
                        [(a, b) for a, b in zip(self, other)],
                    )
                )
            )
        raise TypeError(f"cant sub {self} to {other}")

    def __mul__(self, other: Any | int | float) -> Self:
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] * a_b[1],
                        [
                            (a, b)
                            for a, b in zip(
                                self, cast(Iterable[int | float], other)
                            )
                        ],
                    )
                )
            )
        elif isinstance(other, (float, int)):
            return self.__class__(
                tuple(
                    map(
                        lambda a: a * other,
                        [a for a in self],
                    )
                )
            )

        raise TypeError(f"cant mul {self} to {other}")

    def __truediv__(self, other: Any) -> Self:
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] / a_b[1],
                        [(a, b) for a, b in zip(self, other)],
                    )
                )
            )
        elif isinstance(other, (float, int)):
            return self.__class__(
                tuple(
                    map(
                        lambda a: a / other,
                        [a for a in self],
                    )
                )
            )
        raise TypeError(f"cant div {self} to {other}")

    def __floordiv__(self, other: Any) -> Self:
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] // a_b[1],
                        [(a, b) for a, b in zip(self, other)],
                    )
                )
            )
        elif isinstance(other, (float, int)):
            return self.__class__(
                tuple(
                    map(
                        lambda a: a // other,
                        [a for a in self],
                    )
                )
            )
        raise TypeError(f"cant floordiv {self} to {other}")

    def __iscompatible(self, other: Any) -> bool:
        if (
            hasattr(other, "__iter__")
            and hasattr(other, "__len__")
            and len(other) == self.CLASS_LEN
            and all([isinstance(x, (float, int)) for x in other])
        ):
            return True
        return False

    # def abs_diff(self, other: Any) -> int | float:
    #     if self.__iscompatible(other):
    #         return cast(int | float, sum(...))

    @property
    def pos(self) -> tuple[int | float, ...]:
        return tuple(self._dim_pos)

    def __iter__(self) -> Iterator[int | float]:
        for dim in self._dim_pos:
            yield dim

    def __len__(self) -> int:
        return self.CLASS_LEN

    def __repr__(self) -> str:
        clsname = self.__class__.__name__
        return f"{clsname}({", ".join([str(dim) for dim in self._dim_pos])})"

    def __str__(self) -> str:
        clsname = self.__class__.__name__
        return f"{clsname}({", ".join([str(dim) for dim in self._dim_pos])})"

    def __format__(self, format_spec: Any) -> str:
        result = []
        for i in range(self.CLASS_LEN):
            if self.DIM_ORDER[i] in format_spec:
                result.append(self._dim_pos[i])
        return "(" + " ".join([str(a) for a in result]) + ")"

    def __round__(self, ndigits: Any) -> Self:
        return self.__class__(
            tuple(
                map(
                    lambda s: round(s, ndigits),
                    [a for a in self],
                )
            )
        )

    def __eq__(self, value: Any) -> bool:
        if self.__iscompatible(value):
            return all([(a == b) for a, b in zip(self, value)])
        raise TypeError(f"cant compare {self} to {value}")

    def abs_diff(self, other: Any) -> int | float:
        if self.__iscompatible(other):
            return cast(
                int | float,
                sum(
                    map(
                        lambda a_b: max(a_b) - min(a_b),
                        [(a, b) for a, b in zip(self, other)],
                    )
                ),
            )
        raise TypeError(f"cant floordiv {self} to {other}")

    def __bool__(self) -> bool:
        return any(self._dim_pos)

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __getitem__(
        self, key: Any
    ) -> int | float | tuple[int | float, ...] | Any:
        return self._dim_pos.__getitem__(key)

    def __getattr__(self, name: str) -> int | float | None:
        if name in self.DIM_ORDER[0: self.CLASS_LEN]:
            value = self._dim_pos[self.DIM_ORDER.find(name)]
            return value
        return None


class Pos3d(Vector):
    CLASS_LEN = 3


class Pos4d(Vector):
    CLASS_LEN = 4


class ColorRGBA(Vector):
    CLASS_LEN = 4


# a = Pos3d(1, 2, 3)
# b = Pos3d(5, 2, 3)

# c = Pos4d(1, 2, 3, 4)
# d = ColorRGBA(5, 2, 3, 6)

# print(a)
# print(b)
# print(a + b)

# print(c)
# print(d)
# print(c + d)
# print(a // b)

from pyray import Camera3D, Vector3


class Vector:
    CLASS_LEN = 0
    DIM_ORDER = "xyzabcdef"

    def __init__(self, *args):
        if self.__iscompatible(args):
            self._dim_pos = args
        elif self.__iscompatible(args[0]):
            self._dim_pos = args[0]
        else:
            raise ValueError(
                f"cant initialise {self.__class__.__name__} with {args}"
            )

    def __add__(self, other):
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

    def __sub__(self, other):
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

    def __mul__(self, other):
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] * a_b[1],
                        [(a, b) for a, b in zip(self, other)],
                    )
                )
            )
        raise TypeError(f"cant mul {self} to {other}")

    def __truediv__(self, other):
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] / a_b[1],
                        [(a, b) for a, b in zip(self, other)],
                    )
                )
            )
        raise TypeError(f"cant div {self} to {other}")

    def __floordiv__(self, other):
        if self.__iscompatible(other):
            return self.__class__(
                tuple(
                    map(
                        lambda a_b: a_b[0] // a_b[1],
                        [(a, b) for a, b in zip(self, other)],
                    )
                )
            )
        raise TypeError(f"cant floordiv {self} to {other}")

    def __iscompatible(self, other):
        if (
            hasattr(other, "__iter__")
            and hasattr(other, "__len__")
            and len(other) == self.CLASS_LEN
            and all([isinstance(x, (float, int)) for x in other])
        ):
            return True
        return False

    @property
    def pos(self):
        return tuple(self._dim_pos)

    def __iter__(self):
        for dim in self._dim_pos:
            yield dim

    def __len__(self):
        return self.CLASS_LEN

    def __repr__(self):
        return f"{self.__class__.__name__}({", ".join([str(dim) for dim in self._dim_pos])})"

    def __str__(self):
        return f"{self.__class__.__name__}({", ".join([str(dim) for dim in self._dim_pos])})"

    def __format__(self, format_spec):
        result = []
        for i in range(self.CLASS_LEN):
            if self.DIM_ORDER[i] in format_spec:
                result.append(self._dim_pos[i])
        return "(" + " ".join([str(a) for a in result]) + ")"

    def __round__(self, ndigits=None):
        return self.__class__(
            tuple(
                map(
                    lambda s: round(s, ndigits),
                    [a for a in self],
                )
            )
        )


class Pos3d(Vector):
    CLASS_LEN = 3


class Pos4d(Vector):
    CLASS_LEN = 4


class ColorRGBA(Vector):
    CLASS_LEN = 4


a = Pos3d(1, 2, 3)
b = Pos3d(5, 2, 3)

c = Pos4d(1, 2, 3, 4)
d = ColorRGBA(5, 2, 3, 6)

print(a)
print(b)
print(a + b)

print(c)
print(d)
print(c + d)
print(a // b)
print(
    f"{(((a + (1, 2, 3)) + [1, 2, 3]) + {1: "a", 2: "b", 3: "c"}) + {1, 2, 3}:xz}\n"
    + f"{(((a + (1, 2, 3)) + [1, 2, 3]) + {1: "a", 2: "b", 3: "c"}) + {1, 2, 3}:xyz}"
)

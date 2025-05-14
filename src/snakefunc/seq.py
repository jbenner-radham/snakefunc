from collections.abc import Sequence, Callable
from typing import overload


class Seq[T]:
    def __init__(self, sequence=None) -> None:
        self._value: Sequence[T] = sequence

    def find(self, callback: Callable[[T], bool]) -> T | None:
        for value in self._value:
            if callback(value) is True:
                return value

        return None

    @overload
    def reduce[TAccumulated](
        self, callback: Callable[[TAccumulated, T], TAccumulated], /
    ) -> TAccumulated: ...

    @overload
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated,
    ) -> TAccumulated: ...

    @overload
    def reduce[TAccumulated](
        self, callback: Callable[[TAccumulated, T, int], TAccumulated], /
    ) -> TAccumulated: ...

    @overload
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int], TAccumulated],
        initial_value: TAccumulated,
    ) -> TAccumulated: ...

    @overload
    def reduce[TAccumulated](
        self, callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated], /
    ) -> TAccumulated: ...

    @overload
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated],
        initial_value: TAccumulated,
    ) -> TAccumulated: ...

    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated]
        | Callable[[TAccumulated, T, int], TAccumulated]
        | Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated = None,
    ) -> TAccumulated | None:
        accumulator: TAccumulated = initial_value
        callback_args: tuple[str, ...] = callback.__code__.co_varnames

        if accumulator is None and len(self._value) > 0:
            match self._value[0]:
                case bytes():
                    accumulator = b""
                case float():
                    accumulator = 0.0
                case int():
                    accumulator = 0
                case str():
                    accumulator = ""
                case _:
                    raise TypeError

        match len(callback_args):
            case 4:
                for index, value in enumerate(self._value):
                    accumulator = callback(accumulator, value, index, self._value)
            case 3:
                for index, value in enumerate(self._value):
                    accumulator = callback(accumulator, value, index)
            case 2:
                for value in self._value:
                    accumulator = callback(accumulator, value)
            case _:
                raise TypeError

        return accumulator

    def to_list(self):
        return list(self._value)


def seq[T](sequence: Sequence[T]) -> Seq[T]:
    return Seq(sequence)

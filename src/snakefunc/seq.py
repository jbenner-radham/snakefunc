from collections.abc import Sequence, Callable
from typing import overload, cast, Any, Self


class Seq[T]:
    def __init__(self, sequence=None) -> None:
        self._value: Sequence[T] = sequence

    def find(self, callback: Callable[[T], bool]) -> T | None:
        for value in self._value:
            if callback(value) is True:
                return value

        return None

    def first(self) -> T | None:
        return self._value[0] if len(self._value) > 0 else None

    def last(self) -> T | None:
        return self._value[-1] if len(self._value) > 0 else None

    def len(self) -> int:
        return len(self._value)

    @overload
    def map[TMapped](self, callback: Callable[[T], TMapped]) -> Self: ...

    @overload
    def map[TMapped](self, callback: Callable[[T, int], TMapped]) -> Self: ...

    @overload
    def map[TMapped](
        self, callback: Callable[[T, int, Sequence[T]], TMapped]
    ) -> Self: ...

    def map[TMapped](
        self,
        callback: Callable[[T], TMapped]
        | Callable[[T, int], TMapped]
        | Callable[[T, int, Sequence[T]], TMapped],
    ) -> Self:
        callback_args: tuple[str, ...] = cast(Any, callback).__code__.co_varnames
        sequence: list[T] = []

        match len(callback_args):
            case 3:
                for index, value in enumerate(self._value):
                    sequence.append(callback(value, index, self._value))
            case 2:
                for index, value in enumerate(self._value):
                    sequence.append(callback(value, index))
            case 1:
                for value in self._value:
                    sequence.append(callback(value))
            case _:
                raise TypeError

        self._value = sequence

        return self

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
        callback_args: tuple[str, ...] = cast(Any, callback).__code__.co_varnames

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

    def to_str(self, separator: str | None = None) -> str:
        return (
            "".join(map(str, self.to_list()))
            if separator is None
            else separator.join(map(str, self.to_list()))
        )

    def to_list(self) -> list[T]:
        return list(self._value)


def seq[T](sequence: Sequence[T]) -> Seq[T]:
    return Seq(sequence)

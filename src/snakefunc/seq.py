from collections.abc import Sequence, Callable
from typing import overload, cast, Any, Self, Literal

type RangeType = Literal["range"]
type AcceptableSequenceType = Literal["bytearray", "bytes", "list", "str", "tuple"]
type SequenceType = AcceptableSequenceType | RangeType


class Seq[T]:
    def __init__(
        self, sequence: Sequence[T], coerce_range_into: AcceptableSequenceType = "tuple"
    ) -> None:
        self._value: Sequence[T] = sequence
        self._coerce_range_into: AcceptableSequenceType = coerce_range_into

    def _coerce_range_value(
        self, value: Sequence[T]
    ) -> bytearray | bytes | list[T] | str | tuple[T, ...]:
        match self._coerce_range_into:
            case "bytearray":
                return bytearray(value)
            case "bytes":
                return bytes(value)
            case "list":
                return list(value)
            case "str":
                return "".join(map(str, tuple(value)))
            case "tuple":
                return tuple(value)
            case _:
                raise ValueError()

    def _get_sequence_type(self) -> SequenceType:
        match self._value:
            case bytearray():
                return "bytearray"
            case bytes():
                return "bytes"
            case list():
                return "list"
            case range():
                return "range"
            case str():
                return "str"
            case tuple():
                return "tuple"
            case _:
                raise ValueError()

    @overload
    def filter(self, callback: Callable[[T], bool]) -> Self: ...

    @overload
    def filter(self, callback: Callable[[T, int], bool]) -> Self: ...

    @overload
    def filter(self, callback: Callable[[T, int, Sequence[T]], bool]) -> Self: ...

    def filter(
        self,
        callback: Callable[[T], bool]
        | Callable[[T, int], bool]
        | Callable[[T, int, Sequence[T]], bool],
    ) -> Self:
        if self.len() == 0:
            return self

        callback_args: tuple[str, ...] = callback.__code__.co_varnames
        filtered: list[T] = []
        sequence_type: SequenceType = self._get_sequence_type()

        match len(callback_args):
            case 3:
                for index, value in enumerate(self._value):
                    if callback(value, index, self._value) is True:
                        filtered.append(value)
            case 2:
                for index, value in enumerate(self._value):
                    if callback(value, index) is True:
                        filtered.append(value)
            case 1:
                for value in self._value:
                    if callback(value) is True:
                        filtered.append(value)
            case _:
                raise TypeError

        match sequence_type:
            case "bytearray":
                self._value = bytearray(filtered)
            case "bytes":
                self._value = bytes(filtered)
            case "list":
                self._value = filtered
            case "range":
                self._value = self._coerce_range_value(filtered)
            case "str":
                self._value = "".join(filtered)
            case "tuple":
                self._value = tuple(filtered)

        return self

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


def seq[T](
    sequence: Sequence[T], coerce_range_into: AcceptableSequenceType = "tuple"
) -> Seq[T]:
    return Seq(sequence, coerce_range_into)

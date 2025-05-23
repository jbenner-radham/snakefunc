from collections.abc import Callable, Sequence
from functools import partial
from typing import Any, Literal, Self, cast, overload

type RangeType = Literal["range"]
type CoercibleSequenceType = Literal["bytearray", "bytes", "list", "str", "tuple"]
type SequenceType = CoercibleSequenceType | RangeType


class Seq[T]:
    def __init__(
        self, sequence: Sequence[T], coerce_range_into: CoercibleSequenceType = "tuple"
    ) -> None:
        coercible_sequence_types: tuple[CoercibleSequenceType, ...] = (
            "bytearray",
            "bytes",
            "list",
            "str",
            "tuple",
        )

        if not isinstance(sequence, Sequence):
            raise TypeError(
                'The provided "sequence" argument must be of type "Sequence".'
            )

        if not isinstance(coerce_range_into, str):
            raise TypeError(
                'The provided "coerce_range_into" argument must be of type "str".'
            )

        if not coerce_range_into in coercible_sequence_types:
            raise TypeError(
                'The provided "coerce_range_into" argument must be of type "CoercibleSequenceType" which is a "str" with a value of "bytearray", "bytes", "list", "str", or "tuple".'
            )

        self._value: Sequence[T] = sequence
        self._coerce_range_into: CoercibleSequenceType = coerce_range_into

    @classmethod
    def __call__(cls, *args, **kwargs) -> Self:
        return cls(*args, **kwargs)

    @staticmethod
    def _build_callback_partial(
        callback: Callable[[Any, ...], Any], args: list[Any]
    ) -> Callable[[], Any]:
        callback_args: tuple[str, ...] = callback.__code__.co_varnames
        callback_args_len = len(callback_args)
        max_args_len = len(args)
        exclusive_stop_index = max_args_len + 1

        for index in range(1, exclusive_stop_index):
            if index == callback_args_len:
                return partial(callback, *args[:index])

        raise TypeError(
            f'The "callback" argument callable must have 1 to {max_args_len} arguments.'
        )

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
        match self.value():
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

    def _transform_list_into_sequence_type(self, value: list[T]) -> Sequence[T]:
        match self._get_sequence_type():
            case "bytearray":
                return bytearray(value)
            case "bytes":
                return bytes(value)
            case "list":
                return value
            case "range":
                return self._coerce_range_value(value)
            case "str":
                return "".join(value)
            case "tuple":
                return tuple(value)
            case _:
                raise TypeError(
                    f'Cannot transform list. Non-sequence type of "{self._get_sequence_type()}" specified.'
                )

    @overload
    def all(self, callback: Callable[[T, int, Sequence[T]], bool]) -> Self: ...

    @overload
    def all(self, callback: Callable[[T, int], bool]) -> Self: ...

    @overload
    def all(self, callback: Callable[[T], bool]) -> Self: ...

    def all(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> bool:
        for index, value in enumerate(self.value()):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if not fn():
                return False

        return True

    @overload
    def any(self, callback: Callable[[T, int, Sequence[T]], bool]) -> Self: ...

    @overload
    def any(self, callback: Callable[[T, int], bool]) -> Self: ...

    @overload
    def any(self, callback: Callable[[T], bool]) -> Self: ...

    def any(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> bool:
        for index, value in enumerate(self.value()):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if fn():
                return True

        return False

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

        filtered: list[T] = []

        for index, value in enumerate(self.value()):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if fn() is True:
                filtered.append(value)

        self._value = self._transform_list_into_sequence_type(filtered)

        return self

    def find(self, callback: Callable[[T], bool]) -> T | None:
        for value in self.value():
            if callback(value):
                return value

        return None

    def first(self) -> T | None:
        return self.value()[0] if self.len() > 0 else None

    def last(self) -> T | None:
        return self.value()[-1] if self.len() > 0 else None

    def len(self) -> int:
        return len(self.value())

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
        mapped: list[T] = []

        for index, value in enumerate(self.value()):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            mapped.append(fn())

        self._value = self._transform_list_into_sequence_type(mapped)

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

        if accumulator is None and self.len() > 0:
            match self.first():
                case bytearray():
                    accumulator = bytearray()
                case bytes():
                    accumulator = b""
                case complex():
                    accumulator = complex()
                case dict():
                    accumulator = {}
                case float():
                    accumulator = 0.0
                case frozenset():
                    accumulator = frozenset()
                case int():
                    accumulator = 0
                case set():
                    accumulator = set()
                case str():
                    accumulator = ""
                case _:
                    raise TypeError

        for index, value in enumerate(self.value()):
            args = [accumulator, value, index, self.value()]
            accumulator = self._build_callback_partial(callback, args)()

        return accumulator

    def to_str(self, separator: str | None = None) -> str:
        return (
            "".join(map(str, self.to_list()))
            if separator is None
            else separator.join(map(str, self.to_list()))
        )

    def to_list(self) -> list[T]:
        return list(self.value())

    def to_tuple(self) -> tuple[T, ...]:
        return tuple(self.value())

    def value(self) -> Sequence[T]:
        return self._value


seq = Seq

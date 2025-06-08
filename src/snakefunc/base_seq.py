from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator, Sequence
from functools import partial
from types import FunctionType
from typing import Any, cast, overload

from snakefunc.identity import is_ellipsis
from snakefunc.types import CoercibleSequenceType, SequenceType


class BaseSeq[T]:
    __slots__ = ("_coerce_into", "_value")

    def __init__(
        self, sequence: Sequence[T], coerce_into: CoercibleSequenceType = "tuple"
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

        if not isinstance(coerce_into, str):
            raise TypeError(
                'The provided "coerce_into" argument must be of type "str".'
            )

        if not coerce_into in coercible_sequence_types:
            raise TypeError(
                'The provided "coerce_into" argument must be of type "CoercibleSequenceType" which is a "str" with a value of "bytearray", "bytes", "list", "str", or "tuple".'
            )

        self._value: Sequence[T] = sequence
        self._coerce_into: CoercibleSequenceType = coerce_into

    def __contains__(self, item: T) -> bool:
        """
        Adds compatability for membership test operators.

        :param item: The item to check for in the sequence.
        :return: `True` or `False` depending on if the item is in the sequence.
        """
        return self.value().__contains__(item)

    def __getitem__(self, item: int | slice) -> T:
        """
        Enables getting an item or items from the sequence using an index or slice.

        :param item: The index or slice of the desired item(s).
        :return: The requested item(s) of the sequence.
        """
        return self.value()[item]

    def __iter__(self) -> Iterator[T]:
        """
        Enables iterating over the sequence.

        :return: An iterator of the sequence.
        """
        return iter(self.value())

    def __len__(self) -> int:
        """
        Enables compatibility with the `len()` function.

        :return: The length of the sequence.
        """
        return len(self.value())

    @staticmethod
    def _build_callback_partial(
        callback: Callable[..., Any], args: list[Any], min_args_len: int = 1
    ) -> Callable[[], Any]:
        callback_args: tuple[str, ...] = cast(
            FunctionType, callback
        ).__code__.co_varnames
        callback_args_len = len(callback_args)
        max_args_len = len(args)
        exclusive_stop_index = max_args_len + 1

        for index in range(min_args_len, exclusive_stop_index):
            if index == callback_args_len:
                return partial(callback, *args[:index])

        raise TypeError(
            f'The "callback" argument callable must have {min_args_len} to {max_args_len} arguments.'
        )

    def _build_sequence_from_list(self, value: list[T]) -> Sequence[T]:
        match self._sequence_type:
            case "bytearray":
                return bytearray(value)
            case "bytes":
                return bytes(value)
            case "list":
                return value
            case "range":
                return self._coerce_value(value)
            case "str":
                return "".join(value)
            case "tuple":
                return tuple(value)
            case _:
                raise TypeError(
                    f'Cannot build sequence from list. Non-sequence type of "{self._sequence_type}" specified.'
                )

    def _coerce_value(
        self,
        value: Sequence[T] | None = None,
        into_type: CoercibleSequenceType | None = None,
    ) -> bytearray | bytes | list[T] | str | tuple[T, ...]:
        coerce_from = self.value() if value is None else value
        coerce_into = self._coerce_into if into_type is None else into_type

        match coerce_into:
            case "bytearray":
                return bytearray(coerce_from)
            case "bytes":
                return bytes(coerce_from)
            case "list":
                return list(coerce_from)
            case "str":
                return "".join(map(str, tuple(coerce_from)))
            case "tuple":
                return tuple(coerce_from)
            case _:
                raise TypeError(f'Cannot coerce into unsupported type "{coerce_into}".')

    def _duplicates(self) -> Sequence[T]:
        counts: dict[str, int] = {}
        duplicates: list[T] = []

        for value in self:
            key = str(value)
            counts[key] = counts.get(key, 0) + 1

            if counts.get(key) == 2:
                duplicates.append(value)

        return self._build_sequence_from_list(duplicates)

    def _filter(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> Sequence[T]:
        filtered: list[T] = []

        for index, value in enumerate(self):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if fn():
                filtered.append(value)

        return self._build_sequence_from_list(filtered)

    @property
    def _is_range(self) -> bool:
        return self._sequence_type == "range"

    def _map[TMapped](
        self,
        callback: Callable[[T, int, Sequence[T]], TMapped]
        | Callable[[T, int], TMapped]
        | Callable[[T], TMapped],
    ) -> Sequence[T]:
        mapped: list[T] = []

        for index, value in enumerate(self):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            mapped.append(fn())

        return self._build_sequence_from_list(mapped)

    @property
    def _sequence_type(self) -> SequenceType:
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

    @overload
    @abstractmethod
    def all(self, callback: Callable[[T, int, Sequence[T]], bool]) -> bool: ...

    @overload
    @abstractmethod
    def all(self, callback: Callable[[T, int], bool]) -> bool: ...

    @overload
    @abstractmethod
    def all(self, callback: Callable[[T], bool]) -> bool: ...

    @abstractmethod
    def all(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> bool:
        for index, value in enumerate(self):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if not fn():
                return False

        return True

    @overload
    @abstractmethod
    def any(self, callback: Callable[[T, int, Sequence[T]], bool]) -> bool: ...

    @overload
    @abstractmethod
    def any(self, callback: Callable[[T, int], bool]) -> bool: ...

    @overload
    @abstractmethod
    def any(self, callback: Callable[[T], bool]) -> bool: ...

    @abstractmethod
    def any(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> bool:
        for index, value in enumerate(self):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if fn():
                return True

        return False

    @abstractmethod
    def count(self, item: T, start: int = 0, end: int = ...) -> int:
        # TODO: Revisit the signature of this method. The `Sequence` interface only has the `item`
        #       argument. Should we strictly conform to that?

        if not is_ellipsis(end):
            return cast(bytearray | bytes | str, self.value()).count(item, start, end)

        if start != 0 and is_ellipsis(end):
            return cast(bytearray | bytes | str, self.value()).count(item, start)

        return self.value().count(item)

    @abstractmethod
    def deduplicate(self) -> Sequence[T]:
        counts: dict[str, int] = {}
        unique_items: list[T] = []

        for item in self:
            key = str(item)
            counts[key] = counts.get(key, 0) + 1

            if counts.get(key) == 1:
                unique_items.append(item)

        return self._build_sequence_from_list(unique_items)

    @overload
    @abstractmethod
    def find(self, callback: Callable[[T, int, Sequence[T]], bool]) -> T | None: ...

    @overload
    @abstractmethod
    def find(self, callback: Callable[[T, int], bool]) -> T | None: ...

    @overload
    @abstractmethod
    def find(self, callback: Callable[[T], bool]) -> T | None: ...

    @abstractmethod
    def find(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> T | None:
        for index, value in enumerate(self):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if fn():
                return value

        return None

    @abstractmethod
    def first(self) -> T | None:
        return self[0] if self.len() != 0 else None

    @abstractmethod
    def index(self, item: T, start: int = 0, stop: int | None = None) -> int:
        # Ranges don't support the `start` and `end` arguments even though they're
        # of the `Sequence` type. I'm confused, but here's a workaround regardless.
        sequence = self.value() if not self._is_range else self._coerce_value()

        return (
            sequence.index(item, start, stop)
            if isinstance(stop, int)
            else sequence.index(item, start)
        )

    @abstractmethod
    def join_into_str(self, separator: str | None = None) -> str:
        return (
            "".join(map(str, self))
            if separator is None
            else separator.join(map(str, self))
        )

    @abstractmethod
    def last(self) -> T | None:
        return self[-1] if self.len() != 0 else None

    @abstractmethod
    def len(self) -> int:
        return len(self)

    @overload
    @abstractmethod
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated: ...

    @overload
    @abstractmethod
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated: ...

    @overload
    @abstractmethod
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated: ...

    @abstractmethod
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated]
        | Callable[[TAccumulated, T, int], TAccumulated]
        | Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated:
        accumulator: TAccumulated = initial_value

        if accumulator is None and self.len() != 0:
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
                    raise TypeError(
                        'Cannot auto-create an initial value based on the sequence type. Please provide an "initial_value" argument.'
                    )

        for index, value in enumerate(self):
            args = [accumulator, value, index, self.value()]
            accumulator = self._build_callback_partial(callback, args, min_args_len=2)()

        return accumulator

    @abstractmethod
    def value(self) -> Sequence[T]:
        return self._value

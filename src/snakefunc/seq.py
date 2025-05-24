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

    def __getitem__(self, item: int | slice) -> T:
        """
        Enables getting an item or items from the sequence using an index or slice.

        >>> seq("Hi!")[-1]
        !

        >>> seq("Hi!")[1:]
        i!

        :param item: The index or slice of the desired item(s).
        :type item: int | slice
        :return: The requested item(s) of the sequence.
        :rtype: T
        """
        return self.value()[item]

    def __len__(self) -> int:
        """
        Enables compatability with the `len()` function.

        >>> len(seq("Hi!"))
        3

        :return: The length of the sequence.
        :rtype: int
        """
        return self.len()

    @staticmethod
    def _build_callback_partial(
        callback: Callable[..., Any], args: list[Any], min_args_len: int = 1
    ) -> Callable[[], Any]:
        callback_args: tuple[str, ...] = callback.__code__.co_varnames
        callback_args_len = len(callback_args)
        max_args_len = len(args)
        exclusive_stop_index = max_args_len + 1

        for index in range(min_args_len, exclusive_stop_index):
            if index == callback_args_len:
                return partial(callback, *args[:index])

        raise TypeError(
            f'The "callback" argument callable must have {min_args_len} to {max_args_len} arguments.'
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

    def count(self, item: T, start: int | None = None, end: int | None = None) -> int:
        """
        Get the number of times `item` occurs in the sequence.

        >>> seq([1, 3, 3, 7]).count(3)
        2

        Optionally, sequences of `bytearray`, `bytes`, and `str` types support the `start`
        and `end` arguments. Other types will raise a `TypeError` if they are provided.

        >>> seq[bytes](b"123455555").count(b"5", 0, 5)
        1

        If the `end` argument is specified, then the `start` argument must not be `None`.

        :param item: The item to be counted.
        :type item: T
        :param start: The index to start the count from. Optional, defaults to `None`.
        :type start: int | None
        :param end: The exclusive index to stop the count at. Optional, defaults to `None`.
        :type end: int | None
        :return: The number of times `item` occurs in the sequence.
        :rtype: int
        :raises: TypeError
        """
        if start is None and end is not None:
            raise TypeError(
                'The "start" argument cannot be "None" if the "end" argument is specified.'
            )

        if start is not None and end is not None:
            return cast(bytearray | bytes | str, self.value()).count(item, start, end)

        if start is not None and end is None:
            return cast(bytearray | bytes | str, self.value()).count(item, start)

        return self.value().count(item)

    def deduplicate(self) -> Self:
        """
        Deduplicate the items in the sequence.

        >>> seq((1, 2, 2, 3, 4, 4, 5)).deduplicate().value()
        (1, 2, 3, 4, 5)

        :return: The class instance for method chaining.
        :rtype: Self
        """
        counts: dict[str, int] = {}
        unique_items: list[T] = []

        for item in self.value():
            key = str(item)
            counts[key] = counts.get(key, 0) + 1

            if counts.get(key) == 1:
                unique_items.append(item)

        self._value = self._transform_list_into_sequence_type(unique_items)

        return self

    def duplicates(self) -> Self:
        """
        Find the duplicate values in the sequence.

        :return: The class instance for method chaining.
        :rtype: Self
        """
        counts: dict[str, int] = {}
        duplicates: list[T] = []

        for index, value in enumerate(self.value()):
            key = str(value)
            counts[key] = counts.get(key, 0) + 1

            if counts.get(key) == 2:
                duplicates.append(value)

        self._value = self._transform_list_into_sequence_type(duplicates)

        return self

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

            if fn():
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
            accumulator = self._build_callback_partial(callback, args, min_args_len=2)()

        return accumulator

    def to_bytes(self) -> bytes:
        """
        Get the value of the sequence as bytes.

        :return: A bytes representation of the sequence.
        :rtype: bytes
        """
        return self.to_str().encode()

    def to_list(self) -> list[T]:
        """
        Get the value of the sequence as list.

        :return: A list representation of the sequence.
        :rtype: list[T]
        """
        return list(self.value())

    def to_str(self, separator: str | None = None) -> str:
        """
        Get the value of the sequence as a string. Optionally, joined together with a separator.

        :param separator: If desired, a separator to join the sequence together with. Defaults to `None`.
        :type separator: str | None
        :return: A string representation of the sequence.
        :rtype: str
        """
        return (
            "".join(map(str, self.value()))
            if separator is None
            else separator.join(map(str, self.value()))
        )

    def to_tuple(self) -> tuple[T, ...]:
        """
        Get the value of the sequence as a tuple.

        :return: A tuple representation of the sequence.
        :rtype: tuple[T, ...]
        """
        return tuple(self.value())

    def unique(self) -> Self:
        """
        Find the unique items in the sequence.

        >>> seq((1, 2, 2, 3, 4, 4, 5)).unique().value()
        (1, 3, 5)

        :return: The class instance for method chaining.
        :rtype: Self
        """
        counts: dict[str, int] = {}
        unique_items: list[T] = []

        for item in self.value():
            key = str(item)
            counts[key] = counts.get(key, 0) + 1

            if counts.get(key) == 1:
                unique_items.append(item)
            elif counts.get(key) > 1:
                unique_items.remove(item)

        self._value = self._transform_list_into_sequence_type(unique_items)

        return self

    def value(self) -> Sequence[T]:
        """
        Get the value of the sequence.

        :return: A sequence of values.
        :rtype: Sequence[T]
        """
        return self._value


seq = Seq

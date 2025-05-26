from collections.abc import Callable, Iterator, Sequence
from functools import partial
from types import FunctionType
from typing import Any, Literal, Self, cast, overload

from snakefunc.identity import (
    is_bytearray,
    is_bytes,
    is_ellipsis,
    is_list,
    is_range,
    is_str,
    is_tuple,
)

type RangeType = Literal["range"]
type CoercibleSequenceType = Literal["bytearray", "bytes", "list", "str", "tuple"]
type SequenceType = CoercibleSequenceType | RangeType


class seq[T]:
    __slots__ = ("_coerce_range_into", "_value")

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

    def __add__(self, other: Sequence[T]) -> "seq[T]":
        """
        Adds support for the addition operator. Which, when used with another sequence will return a combination of the
        two.

        >>> seq([1, 2, 3]) + seq([4, 5, 6])

        :param other: The other sequence to be added.
        :type other: Sequence[T]
        :return: A new instance of `seq` containing both sequences combined.
        :rtype: seq[T]
        """

        if self._is_bytearray and is_bytearray(other):
            return seq(
                cast(bytearray, self.value()) + cast(bytearray, other),
                self._coerce_range_into,
            )

        if self._is_bytes and is_bytes(other):
            return seq(
                cast(bytes, self.value()) + cast(bytes, other), self._coerce_range_into
            )

        if self._is_list and is_list(other):
            return seq(
                cast(list[T], self.value()) + cast(list[T], other),
                self._coerce_range_into,
            )

        if self._is_range and is_range(other):
            sequence_self = self._coerce_value(self.value())
            sequence_other = self._coerce_value(other)

            return seq(sequence_self + sequence_other, self._coerce_range_into)

        if self._is_str and is_str(other):
            return seq(
                cast(str, self.value()) + cast(str, other), self._coerce_range_into
            )

        if self._is_tuple and is_tuple(other):
            return seq(
                cast(tuple, self.value()) + cast(tuple, other), self._coerce_range_into
            )

        sequence_type = cast(
            CoercibleSequenceType,
            self._sequence_type if not self._is_range else self._coerce_range_into,
        )
        sequence_self = (
            self.value() if not self._is_range else self._coerce_value(self.value())
        )
        sequence_other = self._coerce_value(other, into_type=sequence_type)

        return seq(sequence_self + sequence_other, self._coerce_range_into)

    def __bool__(self) -> bool:
        """
        Adds compatability for truth value testing.

        >>> bool(seq(["a", "b", "c"]))
        True

        :return: `True` if the sequence length is non-zero, `False` otherwise.
        :rtype: bool
        """
        return self.len() != 0

    @classmethod
    def __call__(cls, *args, **kwargs) -> Self:
        return cls(*args, **kwargs)

    def __contains__(self, item: T) -> bool:
        """
        Adds compatability for membership test operators.

        >>> 5 in seq((1, 2, 3, 4, 5))
        True

        :param item: The item to check for in the sequence.
        :type item: T
        :return: `True` or `False` depending on if the item is in the sequence.
        :rtype: bool
        """
        return self.value().__contains__(item)

    def __delitem__(self, index: int | slice) -> None:
        """
        Adds support for deleting items from the sequence.

        >>> del seq((1, 2, 3, 4, 5))[2]

        :param index: The index or slice of the item(s) in the sequence to delete.
        :type index: int | slice
        :return: Nothing.
        :rtype: None
        """

        if self._is_mutable_type:
            del cast(bytearray | list, self.value())[index]
        elif self._is_range:
            self._value = self._coerce_value(self.value())
            mutable_copy = list(self.value())

            del mutable_copy[index]

            self._value = self._coerce_value(mutable_copy)
        else:
            original_type = cast(CoercibleSequenceType, self._sequence_type)
            mutable_copy = list(self.value())

            del mutable_copy[index]

            self._value = self._coerce_value(mutable_copy, into_type=original_type)

    def __eq__(self, other: Any) -> bool:
        """
        Adds compatability for equality test operators.

        >>> seq([1, 2, 3]) == [1, 2, 3]
        True

        NOTE: This may change in the future, as I'm not certain if checking for
              equality with the internal sequence is how this should be handled.

        :param other: The other object to compare to.
        :type other: Any
        :return: `True` or `False` depending on if the sequence is equal to the other object.
        :rtype: bool
        """
        return self.value() == other

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

    def __iter__(self) -> Iterator[T]:
        """
        Enables iterating over the sequence.

        >>> for value in seq([1, 2, 3]): ...

        :return: An iterator of the sequence.
        :rtype: Iterator[T]
        """
        return iter(self.value())

    def __len__(self) -> int:
        """
        Enables compatability with the `len()` function.

        >>> len(seq("Hi!"))
        3

        :return: The length of the sequence.
        :rtype: int
        """
        return self.len()

    def __ne__(self, other: Any) -> bool:
        """
        Adds compatability for inequality test operators.

        >>> seq([1, 2, 3]) != [4, 5, 6]
        True

        NOTE: This may change in the future, as I'm not certain if checking for
              inequality with the internal sequence is how this should be handled.

        :param other: The other object to compare to.
        :type other: Any
        :return: `True` or `False` depending on if the sequence is not equal to the other object.
        :rtype: bool
        """
        return self.value() != other

    def __reversed__(self) -> Iterator[T]:
        """
        Enables compatability with the `reversed()` function.

        >>> list(reversed(seq([1, 2, 3])))
        [3, 2, 1]

        :return: An iterator of the reversed sequence.
        :rtype: Iterator[T]
        """
        return reversed(self.value())

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

    def _coerce_value(
        self, value: Sequence[T], into_type: CoercibleSequenceType | None = None
    ) -> bytearray | bytes | list[T] | str | tuple[T, ...]:
        coerce_into = self._coerce_range_into if into_type is None else into_type

        match coerce_into:
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
                raise TypeError(f'Cannot coerce into unsupported type "{coerce_into}".')

    @property
    def _is_bytearray(self) -> bool:
        return self._sequence_type == "bytearray"

    @property
    def _is_bytes(self) -> bool:
        return self._sequence_type == "bytes"

    @property
    def _is_list(self) -> bool:
        return self._sequence_type == "list"

    @property
    def _is_mutable_type(self) -> bool:
        return self._sequence_type == ("bytearray", "list")

    @property
    def _is_range(self) -> bool:
        return self._sequence_type == "range"

    @property
    def _is_str(self) -> bool:
        return self._sequence_type == "str"

    @property
    def _is_tuple(self) -> bool:
        return self._sequence_type == "tuple"

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

    def _transform_list_into_sequence_type(self, value: list[T]) -> Sequence[T]:
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
                    f'Cannot transform list. Non-sequence type of "{self._sequence_type}" specified.'
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
        """
        Iterate over the items in the sequence and return a `bool` indicating if all the items match the callback predicate.

        >>> seq([2, 4, 6, 8, 10]).all(lambda number: number % 2 == 0)
        True

        :param callback: A callback predicate which has a value argument, and optionally index and sequence arguments.
        :type callback: Callable[[T, int, Sequence[T]], bool] | Callable[[T, int], bool] | Callable[[T], bool]
        :return: `True` if all the items in the sequence match the callback predicate, `False` otherwise.
        :rtype: bool
        """

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
        """
        Iterate over the items in the sequence and return a `bool` indicating if any item matches the callback predicate.

        >>> seq(("foo", "bar", "baz")).any(lambda item: item == "foo")
        True

        :param callback: A callback predicate which has a value argument, and optionally index and sequence arguments.
        :type callback: Callable[[T, int, Sequence[T]], bool] | Callable[[T, int], bool] | Callable[[T], bool]
        :return: `True` if any item in the sequence matches the callback predicate, `False` otherwise.
        :rtype: bool
        """

        for index, value in enumerate(self.value()):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if fn():
                return True

        return False

    def clear(self) -> None:
        """
        Remove all items from the underlying sequence.

        >>> sequence = seq([1, 2, 3])
        >>> sequence.clear()
        >>> sequence.value()
        []

        TODO: Consider whether we should deviate from the `MutableSequence`
              interface so we can allow chaining.

        :return: Nothing.
        :rtype: None
        """
        del self[:]

    def count(self, item: T, start: int = 0, end: int = ...) -> int:
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
        :param start: The index to start the count from. Optional, defaults to `0`.
        :type start: int
        :param end: The exclusive index to stop the count at. Optional, defaults to `...`.
        :type end: int
        :return: The number of times `item` occurs in the sequence.
        :rtype: int
        :raises TypeError: If `start` and/or `end` arguments are supplied for an incompatible sequence.
        """

        # TODO: Revisit the signature of this method. The `Sequence` interface only has the `item`
        #       argument. Should we strictly conform to that?

        if not is_ellipsis(end):
            return cast(bytearray | bytes | str, self.value()).count(item, start, end)

        if start != 0 and is_ellipsis(end):
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
    def filter(self, callback: Callable[[T, int, Sequence[T]], bool]) -> Self: ...

    @overload
    def filter(self, callback: Callable[[T, int], bool]) -> Self: ...

    @overload
    def filter(self, callback: Callable[[T], bool]) -> Self: ...

    def filter(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> Self:
        """
        Iterate over the sequence and retain the items for which the predicate callback returns `True`.

        >>> seq([1, 2, 3, 4, 5, 6]).filter(lambda number: number % 2 == 0).value()
        [2, 4, 6]

        :param callback: A predicate callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :type callback: Callable[[T, int, Sequence[T]], bool] | Callable[[T, int], bool] | Callable[[T], bool]
        :return: The class instance for method chaining.
        :rtype: Self
        """

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

    @overload
    def find(self, callback: Callable[[T, int, Sequence[T]], bool]) -> Self: ...

    @overload
    def find(self, callback: Callable[[T, int], bool]) -> Self: ...

    @overload
    def find(self, callback: Callable[[T], bool]) -> Self: ...

    def find(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> T | None:
        """
        Iterate over the sequence and return the first item for which the predicate callback returns `True`. Returns
        `None` if nothing is found.

        >>> seq([0, 1, 2, 3, 4, 5, 6]).find(lambda number: number % 2 == 0).value()
        2

        :param callback: A predicate callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :type callback: Callable[[T, int, Sequence[T]], bool] | Callable[[T, int], bool] | Callable[[T], bool]
        :return: The first item found, or `None` if nothing matches.
        :rtype: T
        """

        for index, value in enumerate(self.value()):
            args = [value, index, self.value()]
            fn = self._build_callback_partial(callback, args)

            if fn():
                return value

        return None

    def first(self) -> T | None:
        """
        Returns the first item in the sequence, or `None` if the sequence is empty.

        >>> seq([1, 2, 3, 4, 5]).first()
        1

        :return: The first item in the sequence, or `None` if the sequence is empty.
        :rtype: T
        """
        return self.value()[0] if self.len() > 0 else None

    def index(self, item: T, start: int = 0, stop: int = ...) -> int:
        """
        Returns the index of the first occurrence of `item` in the sequence.

        >>> seq("abc").index("c")
        2

        Optionally, `start` and `stop` arguments can also be provided.

        >>> seq(("foo", "bar", "foo", "foo")).index("foo", 1, 3)
        2

        Note that if the sequence is of the `range` type, then the `start`
        and `stop` arguments are not supported.

        :param item: The item to search for.
        :type item: T
        :param start: The index to start the search from. Optional, defaults to `0`.
        :type start: int
        :param stop: The exclusive index to stop the search at. Optional, defaults to `...`.
        :type stop: int
        :return: The index of the desired item.
        :rtype: int
        """

        # Ranges don't support the `start` and `end` arguments even though they're
        # of the `Sequence` type. I'm confused, but here's a workaround regardless.
        if self._sequence_type == "range" and start == 0 and is_ellipsis(stop):
            return self.value().index(item)

        if isinstance(stop, int):
            return self.value().index(item, start, stop)

        return self.value().index(item, start)

    def last(self) -> T | None:
        """
        Returns the last item in the sequence, or `None` if the sequence is empty.

        >>> seq([1, 2, 3, 4, 5]).last()
        5

        :return: The last item in the sequence, or `None` if the sequence is empty.
        :rtype: T
        """
        return self.value()[-1] if self.len() > 0 else None

    def len(self) -> int:
        """
        Returns the length of the sequence.

        >>> seq([1, 2, 3, 4, 5]).len()
        5

        :return: The length of the sequence.
        :rtype: int
        """
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

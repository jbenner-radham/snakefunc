import json
from collections.abc import Callable, Iterator, Sequence
from functools import partial
from types import FunctionType
from typing import Any, Self, cast, overload

from snakefunc.base_seq import BaseSeq
from snakefunc.identity import (
    is_bytearray,
    is_bytes,
    is_ellipsis,
    is_list,
    is_range,
    is_str,
    is_tuple,
)
from snakefunc.types import CoercibleSequenceType, SequenceType


class seq[T](BaseSeq[T]):
    def __add__(self, other: Sequence[T]) -> "seq[T]":
        """
        Adds support for the addition operator. Which, when used with another sequence will return a combination of the
        two.

        >>> seq([1, 2, 3]) + seq([4, 5, 6]) # doctest: +ELLIPSIS
        <seq.seq object at 0x...>

        :param other: The other sequence to be added.
        :type other: Sequence[T]
        :return: A new instance of `seq` containing both sequences combined.
        :rtype: seq[T]
        """

        if self._is_bytearray and is_bytearray(other):
            return seq(
                cast(bytearray, self.value()) + cast(bytearray, other),
                self._coerce_into,
            )

        if self._is_bytes and is_bytes(other):
            return seq(
                cast(bytes, self.value()) + cast(bytes, other), self._coerce_into
            )

        if self._is_list and is_list(other):
            return seq(
                cast(list[T], self.value()) + cast(list[T], other),
                self._coerce_into,
            )

        if self._is_range and is_range(other):
            sequence_self = self._coerce_value(self.value())
            sequence_other = self._coerce_value(other)

            return seq(sequence_self + sequence_other, self._coerce_into)

        if self._is_str and is_str(other):
            return seq(cast(str, self.value()) + cast(str, other), self._coerce_into)

        if self._is_tuple and is_tuple(other):
            return seq(
                cast(tuple, self.value()) + cast(tuple, other), self._coerce_into
            )

        sequence_type = cast(
            CoercibleSequenceType,
            self._sequence_type if not self._is_range else self._coerce_into,
        )
        sequence_self = (
            self.value() if not self._is_range else self._coerce_value(self.value())
        )
        sequence_other = self._coerce_value(other, into_type=sequence_type)

        return seq(sequence_self + sequence_other, self._coerce_into)

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

    def __str__(self) -> str:
        """
        Enables the ability to return a string representation of the underlying sequence.

        >>> str(seq([1, 2, 3]))
        '[1, 2, 3]'

        :return: A string representation of the sequence.
        :rtype: str
        """

        return str(self.value())

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
    def _is_str(self) -> bool:
        return self._sequence_type == "str"

    @property
    def _is_tuple(self) -> bool:
        return self._sequence_type == "tuple"

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
    def all(self, callback: Callable[[T, int, Sequence[T]], bool]) -> bool: ...

    @overload
    def all(self, callback: Callable[[T, int], bool]) -> bool: ...

    @overload
    def all(self, callback: Callable[[T], bool]) -> bool: ...

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
        :return: `True` if all the items in the sequence match the callback predicate, `False` otherwise.
        """
        return super().all(callback)

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
        :return: `True` if any item in the sequence matches the callback predicate, `False` otherwise.
        """
        return super().any(callback)

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

        :param item: The item to be counted.
        :param start: The index to start the count from. Optional, defaults to `0`.
        :param end: The exclusive index to stop the count at. Optional, defaults to `...`.
        :return: The number of times `item` occurs in the sequence.
        :raises TypeError: If `start` and/or `end` arguments are supplied for an incompatible sequence.
        """
        # TODO: Revisit the signature of this method. The `Sequence` interface only has the `item`
        #       argument. Should we strictly conform to that?
        return super().count(item, start, end)

    def deduplicate(self) -> Self:
        """
        Deduplicate the items in the sequence.

        >>> seq((1, 2, 2, 3, 4, 4, 5)).deduplicate().value()
        (1, 2, 3, 4, 5)

        :return: The class instance for method chaining.
        """
        self._value = super().deduplicate()

        return self

    def duplicates(self) -> Self:
        """
        Find the duplicate values in the sequence.

        >>> seq((1, 2, 2, 3, 4, 4, 5)).duplicates().value()
        (2, 4)

        :return: The class instance for method chaining.
        """
        self._value = super().duplicates()

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
        Iterate over the sequence and retain the items for which the predicate callback returns "truthy".

        >>> seq([1, 2, 3, 4, 5, 6]).filter(lambda number: number % 2 == 0).value()
        [2, 4, 6]

        :param callback: A predicate callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :return: The class instance for method chaining.
        """
        self._value = self._filter(callback)

        return self

    def find(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> T | None:
        """
        Iterate over the sequence and return the first item for which the predicate callback returns `True`. Returns
        `None` if nothing is found.

        >>> seq([1, 2, 3, 4, 5, 6]).find(lambda number: number % 2 == 0)
        2

        :param callback: A predicate callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :return: The first item found, or `None` if nothing matches.
        """
        return super().find(callback)

    def first(self) -> T | None:
        """
        Returns the first item in the sequence, or `None` if the sequence is empty.

        >>> seq([1, 2, 3, 4, 5]).first()
        1

        :return: The first item in the sequence, or `None` if the sequence is empty.
        """
        return super().first()

    def index(self, item: T, start: int = 0, stop: int = ...) -> int:
        """
        Returns the index of the first occurrence of `item` in the sequence.

        >>> seq("abc").index("c")
        2

        Optionally, `start` and `stop` arguments can also be provided.

        >>> seq(("foo", "bar", "foo", "foo")).index("foo", 1, 3)
        2

        Raises a `ValueError` if the item is not in the sequence.

        >>> seq([1, 2, 3]).index(5)
        Traceback (most recent call last):
            ...
        ValueError: 5 is not in list

        :param item: The item to search for.
        :param start: The index to start the search from. Optional, defaults to `0`.
        :param stop: The exclusive index to stop the search at. Optional, defaults to `...`.
        :return: The index of the desired item.
        :raises ValueError: If the item is not in the sequence.
        """
        return super().index(item, start, stop)

    def join_into_str(self, separator: str | None = None) -> str:
        """
        Get the value of the sequence joined into a string.

        >>> seq(["H", "e", "l", "l", "o", "!"]).join_into_str()
        'Hello!'

        Optionally, joined together with a separator.

        >>> seq(("foo", "bar", "baz")).join_into_str(separator=", ")
        'foo, bar, baz'

        :param separator: If desired, a separator to join the sequence together with. Defaults to `None`.
        :return: The sequence joined together as a `str`.
        """
        return super().join_into_str(separator)

    def last(self) -> T | None:
        """
        Returns the last item in the sequence, or `None` if the sequence is empty.

        >>> seq([1, 2, 3, 4, 5]).last()
        5

        :return: The last item in the sequence, or `None` if the sequence is empty.
        """
        return super().last()

    def len(self) -> int:
        """
        Returns the length of the sequence.

        >>> seq([1, 2, 3, 4, 5]).len()
        5

        :return: The length of the sequence.
        """
        return super().len()

    @overload
    def map[TMapped](
        self, callback: Callable[[T, int, Sequence[T]], TMapped]
    ) -> Self: ...

    @overload
    def map[TMapped](self, callback: Callable[[T, int], TMapped]) -> Self: ...

    @overload
    def map[TMapped](self, callback: Callable[[T], TMapped]) -> Self: ...

    def map[TMapped](
        self,
        callback: Callable[[T, int, Sequence[T]], TMapped]
        | Callable[[T, int], TMapped]
        | Callable[[T], TMapped],
    ) -> Self:
        """
        Create a new sequence populated by the results of the callback applied to each item in the current sequence.

        >>> seq([1, 2, 3]).map(lambda number: number * 2).value()
        [2, 4, 6]

        :param callback: A mapper callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :return: The class instance for method chaining.
        """
        self._value = self._map(callback)

        return self

    # @overload
    # def reduce[TAccumulated](
    #     self,
    #     callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated],
    #     initial_value: TAccumulated | None = None,
    # ) -> TAccumulated: ...

    # @overload
    # def reduce[TAccumulated](
    #     self, callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated]
    # ) -> TAccumulated: ...

    # @overload
    # def reduce[TAccumulated](
    #     self,
    #     callback: Callable[[TAccumulated, T, int], TAccumulated],
    #     initial_value: TAccumulated | None = None,
    # ) -> TAccumulated: ...

    # @overload
    # def reduce[TAccumulated](
    #     self, callback: Callable[[TAccumulated, T, int], TAccumulated], /
    # ) -> TAccumulated: ...

    # @overload
    # def reduce[TAccumulated](
    #     self,
    #     callback: Callable[[TAccumulated, T], TAccumulated],
    #     initial_value: TAccumulated | None = None,
    # ) -> TAccumulated: ...

    # @overload
    # def reduce[TAccumulated](
    #     self, callback: Callable[[TAccumulated, T], TAccumulated], /
    # ) -> TAccumulated: ...

    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated]
        | Callable[[TAccumulated, T, int], TAccumulated]
        | Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated:
        """
        Returns the result of the sequence being reduced to a singular value.

        >>> seq([1, 2, 3]).reduce(lambda accumulator, value: accumulator + value)
        6

        An optional `initial_value` argument can be provided to seed the accumulator.

        >>> seq([1, 2, 3]).reduce(lambda accumulator, value: accumulator + value, 5)
        11

        The callback may also optionally include `index` and `sequence` arguments.

        >>> seq([1, 2, 3]).reduce(lambda accumulator, value, index, sequence: accumulator + value + index + len(sequence))
        18

        :param callback: The reducer function. At minimum, it has `accumulator` and `value` arguments.
        :param initial_value: The initial value for the accumulator. If not provided an attempt will be made to supply one.
        :return: The accumulated value.
        """
        return super().reduce(callback, initial_value)

    def to_bytes(self) -> bytes:
        """
        Get the value of the sequence as bytes.

        TODO: Consider returning the sequence as bytes as opposed to joining into a str and encoding into bytes.

        :return: A bytes representation of the sequence.
        :rtype: bytes
        """
        return self.join_into_str().encode()

    def to_list(self) -> list[T]:
        """
        Get the value of the sequence as a list.

        >>> seq("Hi!").to_list()
        ['H', 'i', '!']

        :return: A list representation of the sequence.
        :rtype: list[T]
        """
        return list(self)

    def to_json(self) -> str:
        """
        Get the value of the sequence as a JSON string.

        >>> seq([{"foo": "bar"}, {"baz": "blue"}]).to_json()
        '[{"foo": "bar"}, {"baz": "blue"}]'

        Sequences which are of type `bytearray` or `range` are represented as arrays.

        >>> seq(range(5)).to_json()
        '[0, 1, 2, 3, 4]'

        Lastly, `byte` sequences are represented as strings.

        >>> seq(b"Hi!").to_json()
        '"b\\'Hi!\\'"'

        :return: A JSON representation of the sequence.
        :rtype: str
        """
        if self._is_bytearray or self._is_range:
            return json.dumps(self.to_tuple())
        elif self._is_bytes:
            return json.dumps(self.to_str())

        return json.dumps(self.value())

    def to_str(self) -> str:
        """
        Get the value of the sequence as a string.

        >>> seq([1, 2, 3]).to_str()
        '[1, 2, 3]'

        :return: A string representation of the sequence.
        """

        return str(self)

    def to_tuple(self) -> tuple[T, ...]:
        """
        Get the value of the sequence as a tuple.

        >>> seq(range(3)).to_tuple()
        (0, 1, 2)

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
            elif cast(int, counts.get(key)) > 1:
                unique_items.remove(item)

        self._value = self._transform_list_into_sequence_type(unique_items)

        return self

    def value(self) -> Sequence[T]:
        """
        Get the value of the sequence.

        >>> seq([1, 2, 3]).value()
        [1, 2, 3]

        :return: The underlying sequence.
        """
        return super().value()

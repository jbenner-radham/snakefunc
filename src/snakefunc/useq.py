from collections.abc import Callable, Sequence
from typing import Self, overload

from snakefunc.base_seq import BaseSeq


class useq[T](BaseSeq[T]):
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

        >>> useq([2, 4, 6, 8, 10]).all(lambda number: number % 2 == 0)
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

        >>> useq(("foo", "bar", "baz")).any(lambda item: item == "foo")
        True

        :param callback: A callback predicate which has a value argument, and optionally index and sequence arguments.
        :return: `True` if any item in the sequence matches the callback predicate, `False` otherwise.
        """
        return super().any(callback)

    def count(self, item: T, start: int = 0, end: int | None = None) -> int:
        """
        Get the number of times `item` occurs in the sequence.

        >>> useq([1, 3, 3, 7]).count(3)
        2

        Optionally, sequences of `bytearray`, `bytes`, and `str` types support the `start`
        and `end` arguments. Other types will raise a `TypeError` if they are provided.

        >>> useq[bytes](b"123455555").count(b"5", 0, 5)
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

    def deduplicate(self) -> Sequence[T]:
        """
        Deduplicate the items in the sequence.

        >>> useq((1, 2, 2, 3, 4, 4, 5)).deduplicate()
        (1, 2, 3, 4, 5)

        :return: The deduplicated sequence.
        """
        return self._deduplicate()

    def duplicates(self) -> Sequence[T]:
        """
        Find the duplicate values in the sequence.

        >>> useq((1, 2, 2, 3, 4, 4, 5)).duplicates()
        (2, 4)

        :return: The duplicate values in the sequence.
        """
        return self._duplicates()

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
    ) -> Sequence[T]:
        """
        Iterate over the sequence and retain the items for which the predicate callback returns "truthy".

        >>> useq([1, 2, 3, 4, 5, 6]).filter(lambda number: number % 2 == 0)
        [2, 4, 6]

        :param callback: A predicate callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :return: The filtered sequence.
        """
        return self._filter(callback)

    def find(
        self,
        callback: Callable[[T, int, Sequence[T]], bool]
        | Callable[[T, int], bool]
        | Callable[[T], bool],
    ) -> T | None:
        """
        Iterate over the sequence and return the first item for which the predicate callback returns `True`. Returns
        `None` if nothing is found.

        >>> useq([1, 2, 3, 4, 5, 6]).find(lambda number: number % 2 == 0)
        2

        :param callback: A predicate callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :return: The first item found, or `None` if nothing matches.
        """
        return super().find(callback)

    def first(self) -> T | None:
        """
        Returns the first item in the sequence, or `None` if the sequence is empty.

        >>> useq([1, 2, 3, 4, 5]).first()
        1

        :return: The first item in the sequence, or `None` if the sequence is empty.
        """
        return super().first()

    def index(self, item: T, start: int = 0, stop: int | None = None) -> int:
        """
        Return the index of the first occurrence of `item` in the sequence.

        >>> useq("abc").index("c")
        2

        Optionally, `start` and `stop` arguments can also be provided.

        >>> useq(("foo", "bar", "foo", "foo")).index("foo", 1, 3)
        2

        Raises a `ValueError` if the item is not in the sequence.

        >>> useq([1, 2, 3]).index(5)
        Traceback (most recent call last):
            ...
        ValueError: 5 is not in list

        :param item: The item to search for.
        :param start: The index to start the search from. Optional, defaults to `0`.
        :param stop: The exclusive index to stop the search at. Optional, defaults to `None`.
        :return: The index of the desired item.
        :raise ValueError: If the item is not in the sequence.
        """
        return super().index(item, start, stop)

    def join_into_str(self, separator: str | None = None) -> str:
        """
        Get the value of the sequence joined into a string.

        >>> useq(["H", "e", "l", "l", "o", "!"]).join_into_str()
        'Hello!'

        Optionally, joined together with a separator.

        >>> useq(("foo", "bar", "baz")).join_into_str(separator=", ")
        'foo, bar, baz'

        :param separator: If desired, a separator to join the sequence together with. Defaults to `None`.
        :return: The sequence joined together as a `str`.
        """
        return super().join_into_str(separator)

    def last(self) -> T | None:
        """
        Returns the last item in the sequence, or `None` if the sequence is empty.

        >>> useq([1, 2, 3, 4, 5]).last()
        5

        :return: The last item in the sequence, or `None` if the sequence is empty.
        """
        return super().last()

    def len(self) -> int:
        """
        Returns the length of the sequence.

        >>> useq([1, 2, 3, 4, 5]).len()
        5

        :return: The length of the sequence.
        """
        return super().len()

    @overload
    def map[TMapped](
        self, callback: Callable[[T, int, Sequence[T]], TMapped]
    ) -> Sequence[T]: ...

    @overload
    def map[TMapped](self, callback: Callable[[T, int], TMapped]) -> Sequence[T]: ...

    @overload
    def map[TMapped](self, callback: Callable[[T], TMapped]) -> Sequence[T]: ...

    def map[TMapped](
        self,
        callback: Callable[[T, int, Sequence[T]], TMapped]
        | Callable[[T, int], TMapped]
        | Callable[[T], TMapped],
    ) -> Sequence[TMapped]:
        """
        Create a new sequence populated by the results of the callback applied to each item in the current sequence.

        >>> useq([1, 2, 3]).map(lambda number: number * 2)
        [2, 4, 6]

        :param callback: A mapper callback which has a `value` argument, and optionally `index` and `sequence` arguments.
        :return: The newly created sequence.
        """
        return self._map(callback)

    @overload
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated: ...

    @overload
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated: ...

    @overload
    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated: ...

    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated]
        | Callable[[TAccumulated, T, int], TAccumulated]
        | Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated | None = None,
    ) -> TAccumulated:
        """
        Returns the result of the sequence being reduced to a singular value.

        >>> useq([1, 2, 3]).reduce(lambda accumulator, value: accumulator + value)
        6

        An optional `initial_value` argument can be provided to seed the accumulator.

        >>> useq([1, 2, 3]).reduce(lambda accumulator, value: accumulator + value, 5)
        11

        The callback may also optionally include `index` and `sequence` arguments.

        >>> useq([1, 2, 3]).reduce(lambda accumulator, value, index, sequence: accumulator + value + index + len(sequence))
        18

        :param callback: The reducer function. At minimum, it has `accumulator` and `value` arguments.
        :param initial_value: The initial value for the accumulator. If not provided an attempt will be made to supply one.
        :return: The accumulated value.
        """
        return super().reduce(callback, initial_value)

    def value(self) -> Sequence[T]:
        """
        Get the value of the sequence.

        >>> useq([1, 2, 3]).value()
        [1, 2, 3]

        :return: The underlying sequence.
        """
        return super().value()

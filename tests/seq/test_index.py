from expects import equal, expect

from snakefunc import seq


def test_index_with_a_range() -> None:
    result = seq(range(10)).index(5)

    expect(result).to(equal(5))


def test_index_with_a_str() -> None:
    result = seq("abc").index("c")

    expect(result).to(equal(2))


def test_index_with_a_tuple_of_strs() -> None:
    result = seq(("foo", "bar", "baz")).index("baz")

    expect(result).to(equal(2))


def test_index_with_a_start_argument_and_a_tuple_of_strs() -> None:
    result = seq(("foo", "foo", "bar")).index("foo", 1)

    expect(result).to(equal(1))


def test_index_with_start_and_end_arguments_and_a_tuple_of_strs() -> None:
    result = seq(("foo", "bar", "foo", "foo")).index("foo", 1, 3)

    expect(result).to(equal(2))

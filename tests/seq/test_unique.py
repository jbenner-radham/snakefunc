from expects import equal, expect

from snakefunc import seq


def test_unique_with_a_list_of_strs() -> None:
    result = seq(["foo", "bar", "baz", "foo"]).unique().value()

    expect(result).to(equal(["bar", "baz"]))


def test_unique_with_a_range() -> None:
    result = seq(range(1, 6)).unique().value()

    expect(result).to(equal((1, 2, 3, 4, 5)))


def test_unique_with_a_tuple_of_ints() -> None:
    result = seq((1, 2, 2, 3, 4, 4, 5)).unique().value()

    expect(result).to(equal((1, 3, 5)))


def test_unique_with_a_str() -> None:
    result = seq("Hello!").unique().value()

    expect(result).to(equal("Heo!"))

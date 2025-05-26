from expects import equal, expect

from snakefunc import seq


def test_clear_with_a_range() -> None:
    result = seq(range(10))

    result.clear()

    expect(result.value()).to(equal(()))


def test_clear_with_a_str() -> None:
    result = seq("Hello, world!")

    result.clear()

    expect(result.value()).to(equal(""))


def test_clear_with_a_list_of_floats() -> None:
    result = seq([1.1, 2.2, 3.3])

    result.clear()

    expect(result.value()).to(equal([]))

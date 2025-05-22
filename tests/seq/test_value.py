from expects import equal, expect

from snakefunc import seq


def test_value_returns_a_collected_bytearray() -> None:
    value = bytearray([1, 2, 3])

    expect(seq(value).value()).to(equal(value))


def test_value_returns_collected_bytes() -> None:
    value = b"Hello, world!"

    expect(seq(value).value()).to(equal(value))


def test_value_returns_a_collected_list() -> None:
    value = [1, 2, 3]

    expect(seq(value).value()).to(equal(value))


def test_value_returns_a_collected_range() -> None:
    value = range(10)

    expect(seq(value).value()).to(equal(value))


def test_value_returns_a_collected_str() -> None:
    value = "Hello, world!"

    expect(seq(value).value()).to(equal(value))


def test_value_returns_a_collected_tuple() -> None:
    value = (1, 2, 3)

    expect(seq(value).value()).to(equal(value))

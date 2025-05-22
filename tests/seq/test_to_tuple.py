from expects import equal, expect

from snakefunc import seq


def test_to_tuple_with_a_bytearray() -> None:
    value = bytearray([1, 0, 1, 1])
    result = seq(value).to_tuple()

    expect(result).to(equal((1, 0, 1, 1)))


def test_to_tuple_with_bytes() -> None:
    value = b"Hi!"
    result = seq(value).to_tuple()

    expect(result).to(equal((ord("H"), ord("i"), ord("!"))))


def test_to_tuple_with_a_list() -> None:
    value = [1, 2, 3, 4, 5]
    result = seq(value).to_tuple()

    expect(result).to(equal((1, 2, 3, 4, 5)))


def test_to_tuple_with_a_range() -> None:
    value = range(5)
    result = seq(value).to_tuple()

    expect(result).to(equal((0, 1, 2, 3, 4)))


def test_to_tuple_with_a_str() -> None:
    value = "Hello!"
    result = seq(value).to_tuple()

    expect(result).to(equal(("H", "e", "l", "l", "o", "!")))

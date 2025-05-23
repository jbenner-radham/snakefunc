from expects import equal, expect

from snakefunc import seq


def test_to_bytes_from_a_bytearray() -> None:
    value = bytearray([8, 8, 8, 8])
    result = seq(value).to_bytes()

    expect(result).to(equal(b"8888"))


def test_to_bytes_from_a_list_of_strs() -> None:
    value = ["foo", "-", "bar", "-", "baz"]
    result = seq(value).to_bytes()

    expect(result).to(equal(b"foo-bar-baz"))


def test_to_bytes_from_a_range() -> None:
    value = range(1, 6)
    result = seq(value).to_bytes()

    expect(result).to(equal(b"12345"))


def test_to_bytes_from_a_str() -> None:
    value = "hello world"
    result = seq(value).to_bytes()

    expect(result).to(equal(b"hello world"))


def test_to_bytes_from_a_tuple_of_ints() -> None:
    value = (1, 2, 3)
    result = seq(value).to_bytes()

    expect(result).to(equal(b"123"))

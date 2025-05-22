from expects import be_false, be_true, expect

from snakefunc import seq


def test_all_with_a_falsy_bytearray() -> None:
    value = bytearray([1, 0, 0, 1])
    result = seq(value).all(lambda byte: byte)

    expect(result).to(be_false)


def test_all_with_a_truthy_bytearray() -> None:
    value = bytearray([1, 1, 1, 1, 1])
    result = seq(value).all(lambda byte: byte)

    expect(result).to(be_true)


def test_all_with_truthy_bytes() -> None:
    value = b"Hello, world!"
    result = seq(value).all(lambda byte: byte)

    expect(result).to(be_true)


def test_all_with_a_falsy_list() -> None:
    value = ["foo", "bar", "baz", ""]
    result = seq(value).all(lambda word: word)

    expect(result).to(be_false)


def test_all_with_a_truthy_list() -> None:
    value = ["hello", "world"]
    result = seq(value).all(lambda word: word)

    expect(result).to(be_true)


def test_all_with_a_falsy_range() -> None:
    value = range(5)
    result = seq(value).all(lambda number: number)

    expect(result).to(be_false)


def test_all_with_a_truthy_range() -> None:
    value = range(1, 5)
    result = seq(value).all(lambda number: number)

    expect(result).to(be_true)


def test_all_with_a_truthy_str() -> None:
    value = "Hello, world!"
    result = seq(value).all(lambda char: char)

    expect(result).to(be_true)


def test_all_with_a_falsy_tuple() -> None:
    value = ("foo", "bar", "baz", "")
    result = seq(value).all(lambda word: word)

    expect(result).to(be_false)


def test_all_with_a_truthy_tuple() -> None:
    value = ("hello", "world")
    result = seq(value).all(lambda word: word)

    expect(result).to(be_true)

from expects import equal, expect

from snakefunc import seq


def test_to_json_with_a_bytearray() -> None:
    result = seq(bytearray([1, 0, 0, 1])).to_json()

    expect(result).to(equal("[1, 0, 0, 1]"))


def test_to_json_with_a_list_of_dicts() -> None:
    result = seq([{"foo": "bar"}, {"baz": "blue"}]).to_json()

    expect(result).to(equal('[{"foo": "bar"}, {"baz": "blue"}]'))


def test_to_json_with_bytes() -> None:
    result = seq(b"Hi!").to_json()

    expect(result).to(equal("\"b'Hi!'\""))


def test_to_json_with_a_range() -> None:
    result = seq(range(5)).to_json()

    expect(result).to(equal("[0, 1, 2, 3, 4]"))


def test_to_json_with_str() -> None:
    result = seq("Hi!").to_json()

    expect(result).to(equal('"Hi!"'))

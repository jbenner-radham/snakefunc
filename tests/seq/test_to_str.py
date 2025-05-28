from expects import equal, expect

from snakefunc import seq


def test_to_str_with_a_list_of_ints() -> None:
    result = seq([1, 2, 3]).to_str()

    expect(result).to(equal("[1, 2, 3]"))


def test_to_str_with_a_range() -> None:
    result = seq(range(5)).to_str()

    expect(result).to(equal("range(0, 5)"))


def test_to_str_with_a_str() -> None:
    result = seq("Hello, World!").to_str()

    expect(result).to(equal("Hello, World!"))

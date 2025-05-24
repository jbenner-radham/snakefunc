from expects import equal, expect

from snakefunc import seq


def test_deduplicate_with_a_list_of_floats() -> None:
    result = seq([1.337, 5.55, 1.337, 2.14]).deduplicate().value()

    expect(result).to(equal([1.337, 5.55, 2.14]))


def test_deduplicate_with_a_str() -> None:
    result = seq("Hello, world!").deduplicate().value()

    expect(result).to(equal("Helo, wrd!"))


def test_deduplicate_with_a_tuple_of_ints() -> None:
    result = seq((1, 2, 2, 3, 4, 4, 5)).deduplicate().value()

    expect(result).to(equal((1, 2, 3, 4, 5)))

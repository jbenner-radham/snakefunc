from expects import be_none, be_true, equal, expect

from snakefunc import seq


def test_contains_dunder_method_with_a_str() -> None:
    expect("foo" in seq("foo bar baz")).to(be_true)


def test_contains_dunder_method_with_a_tuple_of_ints() -> None:
    expect(5 in seq((1, 2, 3, 4, 5))).to(be_true)


def test_eq_dunder_method_with_another_seq_using_the_equal_to_operator() -> None:
    value = (1, 2, 3, 4, 5)

    expect(seq(value) == seq(value)).to(be_true)


def test_eq_dunder_method_with_a_tuple_of_ints() -> None:
    value = (1, 2, 3, 4, 5)

    expect(seq(value)).to(equal(value))


def test_getitem_dunder_method_with_an_index() -> None:
    expect(seq((1, 2, 3))[-1]).to(equal(3))


def test_getitem_dunder_method_with_a_slice() -> None:
    expect(seq((1, 2, 3))[1:]).to(equal((2, 3)))


def test_iter_dunder_method_with_a_str() -> None:
    result: list[str] = []

    for value in seq(["foo", "bar", "baz"]):
        result.append(value)

    expect(result).to(equal(["foo", "bar", "baz"]))


def test_iter_dunder_method_with_a_range() -> None:
    result: list[int] = []

    for value in seq(range(6)):
        result.append(value)

    expect(result).to(equal([0, 1, 2, 3, 4, 5]))


def test_iter_dunder_method_with_a_tuple_of_floats() -> None:
    result: list[float] = []

    for value in seq((5.55, 1.337)):
        result.append(value)

    expect(result).to(equal([5.55, 1.337]))


def test_len_dunder_method_with_a_str() -> None:
    expect(len(seq("Hello!"))).to(equal(6))


def test_len_dunder_method_with_a_tuple() -> None:
    expect(len(seq((3, 4, 5)))).to(equal(3))


def test_reversed_dunder_method_with_a_list_of_ints() -> None:
    result: list[int] = []

    for value in reversed(seq([1, 2, 3, 4, 5])):
        result.append(value)

    expect(result).to(equal([5, 4, 3, 2, 1]))


def test_reversed_dunder_method_with_a_str() -> None:
    result = tuple(reversed(seq("Hello!")))

    expect(result).to(equal(("!", "o", "l", "l", "e", "H")))


def test_first_with_an_empty_list() -> None:
    result = seq([]).first()

    expect(result).to(be_none)


def test_first_with_a_list_of_ints() -> None:
    result = seq([1, 2, 3]).first()

    expect(result).to(equal(1))


def test_last_with_an_empty_list() -> None:
    result = seq([]).last()

    expect(result).to(be_none)


def test_last_with_a_list_of_ints() -> None:
    result = seq([1, 2, 3]).last()

    expect(result).to(equal(3))


def test_len_with_an_empty_list() -> None:
    result = seq([]).len()

    expect(result).to(equal(0))


def test_len_with_a_list_of_ints() -> None:
    result = seq([1, 2, 3]).len()

    expect(result).to(equal(3))


def test_seq_reduce_using_a_lambda_with_two_args_without_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(lambda accumulator, value: accumulator + value)

    expect(result).to(equal(5))


def test_seq_reduce_using_a_lambda_with_two_args_and_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value: accumulator + value, 10
    )

    expect(result).to(equal(15))


def test_seq_reduce_using_a_lambda_with_three_args_without_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index: accumulator + value + index
    )

    expect(result).to(equal(15))


def test_seq_reduce_using_a_lambda_with_three_args_with_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index: accumulator + value + index, 10
    )

    expect(result).to(equal(25))


def test_seq_reduce_using_a_lambda_with_four_args_without_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index, sequence: accumulator
        + value
        + index
        + len(sequence)
    )

    expect(result).to(equal(40))


def test_seq_reduce_using_a_lambda_with_four_args_with_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index, sequence: accumulator
        + value
        + index
        + len(sequence),
        10,
    )

    expect(result).to(equal(50))

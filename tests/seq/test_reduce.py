from expects import equal, expect

from snakefunc import seq


def test_reduce_using_a_lambda_with_two_args_without_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(lambda accumulator, value: accumulator + value)

    expect(result).to(equal(5))


def test_reduce_using_a_lambda_with_two_args_and_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value: accumulator + value, 10
    )

    expect(result).to(equal(15))


def test_reduce_using_a_lambda_with_three_args_without_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index: accumulator + value + index
    )

    expect(result).to(equal(15))


def test_reduce_using_a_lambda_with_three_args_with_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index: accumulator + value + index, 10
    )

    expect(result).to(equal(25))


def test_reduce_using_a_lambda_with_four_args_without_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index, sequence: accumulator
        + value
        + index
        + len(sequence)
    )

    expect(result).to(equal(40))


def test_reduce_using_a_lambda_with_four_args_with_an_initial_value() -> None:
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index, sequence: accumulator
        + value
        + index
        + len(sequence),
        10,
    )

    expect(result).to(equal(50))

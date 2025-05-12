from expects import equal, expect

from snakefunc import seq


def test_seq_reduce_using_a_lambda_with_two_args():
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value: accumulator + value, 10
    )

    expect(result).to(equal(15))


def test_seq_reduce_using_a_lambda_with_three_args():
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index: accumulator + value + index, 10
    )

    expect(result).to(equal(25))


def test_seq_reduce_using_a_lambda_with_four_args():
    result = seq([1, 1, 1, 1, 1]).reduce(
        lambda accumulator, value, index, sequence: accumulator
        + value
        + index
        + len(sequence),
        10,
    )

    expect(result).to(equal(50))

from expects import equal, expect

from snakefunc import seq


def test_find_using_a_lambda_with_a_list_of_dicts() -> None:
    objects = [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "bar"},
    ]
    result = seq(objects).find(lambda obj: obj["name"] == "foo")

    expect(result).to(equal({"id": 1, "name": "foo"}))


def test_find_using_a_fn_with_a_list_of_dicts() -> None:
    objects = [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "bar"},
    ]

    def is_foo[T](obj: T) -> bool:
        return obj["name"] == "foo"

    result = seq(objects).find(is_foo)

    expect(result).to(equal({"id": 1, "name": "foo"}))


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

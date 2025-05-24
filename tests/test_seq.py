from expects import be_none, equal, expect

from snakefunc import seq


def test_getitem_dunder_method_with_an_index() -> None:
    expect(seq((1, 2, 3))[-1]).to(equal(3))


def test_getitem_dunder_method_with_a_slice() -> None:
    expect(seq((1, 2, 3))[1:]).to(equal((2, 3)))


def test_find_using_a_lambda_with_a_list_of_dicts() -> None:
    objects = [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "bar"},
    ]
    result = seq(objects).find(lambda obj: obj["name"] == "foo")

    expect(result).to(equal({"id": 1, "name": "foo"}))


def test_find_using_a_lambda_looking_for_an_object_that_does_not_exist() -> None:
    objects = [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "bar"},
    ]
    result = seq(objects).find(lambda obj: obj["name"] == "baz")

    expect(result).to(be_none)


def test_find_using_a_fn_with_a_list_of_dicts() -> None:
    objects = [
        {"id": 1, "name": "foo"},
        {"id": 2, "name": "bar"},
    ]

    def is_foo[T](obj: T) -> bool:
        return obj["name"] == "foo"

    result = seq(objects).find(is_foo)

    expect(result).to(equal({"id": 1, "name": "foo"}))


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

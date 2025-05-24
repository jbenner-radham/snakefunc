from expects import be_a, equal, expect

from snakefunc import seq


def test_filter_with_a_lambda_with_one_argument() -> None:
    objects = [{"name": "foo", "id": 1}, {"name": "bar", "id": 2}]
    result = seq(objects).filter(lambda obj: obj["name"] == "foo")

    expect(result).to(be_a(seq))


def test_filter_with_a_lambda_with_one_argument_and_converted_to_list() -> None:
    objects = [{"name": "foo", "id": 1}, {"name": "bar", "id": 2}]
    result = seq(objects).filter(lambda obj: obj["name"] == "foo").to_list()

    expect(result).to(equal([{"name": "foo", "id": 1}]))


def test_filter_with_a_lambda_with_two_arguments_and_converted_to_list() -> None:
    objects = [{"name": "foo", "id": 1}, {"name": "bar", "id": 2}]
    result = (
        seq(objects)
        .filter(lambda obj, index: obj["name"] == "foo" and index == 0)
        .to_list()
    )

    expect(result).to(equal([{"name": "foo", "id": 1}]))


def test_filter_with_a_lambda_with_three_arguments_and_converted_to_list() -> None:
    objects = [
        {"name": "foo", "id": 1},
        {"name": "bar", "id": 2},
        {"name": "baz", "id": 3},
    ]
    result = (
        seq(objects)
        .filter(
            lambda obj, index, sequence: index == len(sequence) - 1
            or obj["name"] == "foo"
            and index == 0
        )
        .to_list()
    )

    expect(result).to(equal([{"name": "foo", "id": 1}, {"name": "baz", "id": 3}]))

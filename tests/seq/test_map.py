from expects import be_a, equal, expect

from snakefunc import seq


def test_map_with_a_lambda_with_one_argument() -> None:
    objects = [{"name": "foo", "id": 1}, {"name": "bar", "id": 2}]
    result = seq(objects).map(lambda obj: obj["name"])

    expect(result).to(be_a(seq))


def test_map_with_a_lambda_with_one_argument_and_converted_to_list() -> None:
    objects = [{"name": "foo", "id": 1}, {"name": "bar", "id": 2}]
    result = seq(objects).map(lambda obj: obj["name"]).to_list()

    expect(result).to(equal(["foo", "bar"]))


def test_map_with_a_lambda_with_two_arguments_and_converted_to_list() -> None:
    objects = [{"name": "foo", "id": 1}, {"name": "bar", "id": 2}]
    result = (
        seq(objects)
        .map(lambda obj, index: obj["name"] if index == 0 else "baz")
        .to_list()
    )

    expect(result).to(equal(["foo", "baz"]))


def test_map_with_a_lambda_with_three_arguments_and_converted_to_list() -> None:
    objects = [
        {"name": "foo", "id": 1},
        {"name": "bar", "id": 2},
        {"name": "baz", "id": 3},
    ]
    result = (
        seq(objects)
        .map(
            lambda obj, index, sequence: "foo-bar-baz"
            if index == len(sequence) - 1
            else obj["name"]
        )
        .to_list()
    )

    expect(result).to(equal(["foo", "bar", "foo-bar-baz"]))

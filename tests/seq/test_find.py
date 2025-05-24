from expects import be_none, equal, expect

from snakefunc import seq


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

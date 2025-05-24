from expects import equal, expect

from snakefunc import seq


def test_duplicates_with_a_list_of_ints() -> None:
    value = [1, 2, 3, 4, 5, 6, 7, 1, 3, 3, 7]
    result = seq(value).duplicates().value()

    expect(result).to(equal([1, 3, 7]))


def test_duplicates_with_a_list_of_strs() -> None:
    value = ["hello", "world", "hello", "again", "hello", "always"]
    result = seq(value).duplicates().value()

    expect(result).to(equal(["hello"]))


def test_duplicates_with_a_str() -> None:
    value = "hello"
    result = seq(value).duplicates().value()

    expect(result).to(equal("l"))


def test_duplicates_with_a_tuple_of_ints() -> None:
    value = (1, 2, 3, 1, 2, 3, 4, 5)
    result = seq(value).duplicates().value()

    expect(result).to(equal((1, 2, 3)))


def test_duplicates_with_a_tuple_of_strs() -> None:
    value = ("foo", "bar", "baz", "foo", "baz")
    result = seq(value).duplicates().value()

    expect(result).to(equal(("foo", "baz")))


def test_duplicates_with_a_tuple_of_unique_strs() -> None:
    value = ("lorem", "ipsum", "dolor", "sit", "amet")
    result = seq(value).duplicates().value()

    expect(result).to(equal(()))

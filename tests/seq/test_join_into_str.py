from expects import equal, expect

from snakefunc import seq


def test_join_into_str_with_an_empty_list_and_no_separator() -> None:
    result = seq([]).join_into_str()

    expect(result).to(equal(""))


def test_join_into_str_with_an_empty_list_and_a_separator() -> None:
    result = seq([]).join_into_str(separator=";")

    expect(result).to(equal(""))


def test_join_into_str_with_a_list_of_ints_and_no_separator() -> None:
    result = seq([8, 6, 7, 5, 3, 0, 9]).join_into_str()

    expect(result).to(equal("8675309"))


def test_join_into_str_with_a_list_of_ints_and_a_separator() -> None:
    result = seq([8, 6, 7, 5, 3, 0, 9]).join_into_str(separator=":")

    expect(result).to(equal("8:6:7:5:3:0:9"))

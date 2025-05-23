from expects import be_true, expect

from snakefunc import seq


def test_any_with_a_str_and_a_lambda_with_one_arg() -> None:
    value = "Hello, world!"
    result = seq(value).any(lambda char: char.isalnum())

    expect(result).to(be_true)


def test_any_with_a_str_and_a_lambda_with_two_args() -> None:
    value = "Hello, world!"
    result = seq(value).any(lambda char, index: char.isalnum() and index != 5)

    expect(result).to(be_true)


def test_any_with_a_str_and_a_lambda_with_three_args() -> None:
    value = "Hello, world!"
    result = seq(value).any(
        lambda char, index, sequence: char.isalnum()
        and index != 5
        and len(sequence) > 5
    )

    expect(result).to(be_true)

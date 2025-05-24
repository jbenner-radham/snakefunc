from expects import equal, expect

from snakefunc import seq


def test_count_with_bytes_with_a_start_index() -> None:
    result = seq[bytes](b"123455555").count(b"5", 5)

    expect(result).to(equal(4))


def test_count_with_bytes_with_start_and_end_indexes() -> None:
    result = seq[bytes](b"123455555").count(b"5", 0, 5)

    expect(result).to(equal(1))


def test_count_with_a_list_of_ints() -> None:
    result = seq([1, 3, 3, 7]).count(3)

    expect(result).to(equal(2))

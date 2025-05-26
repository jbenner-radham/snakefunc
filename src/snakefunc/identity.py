from typing import Any


def is_bytearray(value: Any) -> bool:
    return isinstance(value, bytearray)


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes)


def is_ellipsis(value: Any) -> bool:
    return type(value).__name__ == "ellipsis"


def is_list(value: Any) -> bool:
    return isinstance(value, list)


def is_range(value: Any) -> bool:
    return isinstance(value, range)


def is_str(value: Any) -> bool:
    return isinstance(value, str)


def is_tuple(value: Any) -> bool:
    return isinstance(value, tuple)

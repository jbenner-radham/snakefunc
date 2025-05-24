from typing import Any


def is_bytes(value: Any) -> bool:
    return isinstance(value, bytes)


def is_ellipsis(value: Any) -> bool:
    return type(value).__name__ == "ellipsis"


def is_str(value: Any) -> bool:
    return isinstance(value, str)

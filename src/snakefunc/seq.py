from collections.abc import Sequence, Callable


class Seq[T]:
    def __init__(self, sequence=None):
        self.value: Sequence[T] = sequence

    def find(self, callback: Callable[[T], bool]) -> T:
        for value in self.value:
            if callback(value) is True:
                return value

        return None

    def reduce[TAccumulated](
        self,
        callback: Callable[[TAccumulated, T, int, Sequence[T]], TAccumulated]
        | Callable[[TAccumulated, T, int], TAccumulated]
        | Callable[[TAccumulated, T], TAccumulated],
        initial_value: TAccumulated = None,
    ) -> TAccumulated:
        accumulator = initial_value
        callback_args = callback.__code__.co_varnames

        match len(callback_args):
            case 4:
                for index, value in enumerate(self.value):
                    accumulator = callback(accumulator, value, index, self.value)
            case 3:
                for index, value in enumerate(self.value):
                    accumulator = callback(accumulator, value, index)
            case 2:
                for value in self.value:
                    accumulator = callback(accumulator, value)
            case _:
                raise TypeError

        return accumulator

    def to_list(self):
        return list(self.value)


def seq[T](sequence: Sequence[T]) -> Seq[T]:
    return Seq[T](sequence)

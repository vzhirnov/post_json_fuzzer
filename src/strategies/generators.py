import uuid
from typing import Callable


def int_nums_in_range(first: int, second: int):
    return [x for x in range(first, second)]


class Repeater:
    def __init__(self, func: Callable):
        self.value = func

    def __call__(self):
        return self.value()

    def __iter__(self):
        return self

    def __next__(self):
        return self.value()

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(" f"{self.value.__name__!r})"
        )

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.value == other.value


get_new_uuid = (lambda: str(uuid.uuid4()))

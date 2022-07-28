import uuid

import collections.abc

from typing import Generator, Callable


def extract_here(lst: list):
    return lst


class Fuzzy:
    def __init__(
        self,
        default_value,
        data_set: tuple,
        test_methods=None,
        suspicious_responses=None,
        enabled=True,
        description=None,
    ):
        self.obj_id = str(uuid.uuid4())
        self.default_value = None

        self.enabled = enabled

        self.data_set = tuple()
        self.test_methods = test_methods
        self.suspicious_responses = suspicious_responses
        self.tape = None
        self.description = description

        if enabled:
            self.test_methods = test_methods

            if suspicious_responses is None:
                suspicious_responses = []
            self.suspicious_responses = suspicious_responses

            if any(isinstance(x, Callable) for x in data_set):
                self.data_set = next((x for x in data_set if isinstance(x, Callable)), None)
                self.default_value = self.data_set()
                self.tape = [self.data_set]
            else:
                self.default_value = default_value
                self.data_set = tuple([default_value]) + data_set
                self.tape = self.make_tape()
        else:
            self.default_value = default_value

    def make_tape(self):
        s = set()
        s_str = set()
        lst = []
        for item in self.data_set:
            if isinstance(item, collections.Hashable):
                s.add(item)
            else:
                s_item = str(item)
                if s_item not in s_str:
                    s_str.add(s_item)
                    lst.append(item)
                else:
                    continue
        return lst + list(s)

    def get_itself(self):
        return self

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(" f"{self.default_value!r}-{self.obj_id[:6]!r})"
        )

    def __hash__(self):
        return hash((self.obj_id, self.default_value))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.obj_id == other.obj_id

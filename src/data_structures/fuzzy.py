import uuid

import collections.abc


def extract_here(lst: list):
    return lst


class Fuzzy:
    def __init__(
        self,
        default_value,
        data_set: tuple,
        test_method=None,
        suspicious_responses=None,
    ):
        self.obj_id = str(uuid.uuid4())

        self.default_value = default_value
        self.data_set = tuple([default_value]) + data_set
        self.test_method = test_method

        if suspicious_responses is None:
            suspicious_responses = []
        self.suspicious_responses = suspicious_responses

        self.tape = self.make_tape()

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

    def __repr__(self):
        return f'{self.__class__.__name__}('f'{self.default_value!r}-{self.obj_id[:6]!r})'

    def __hash__(self):
        return hash((self.obj_id, self.default_value))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.obj_id == other.obj_id

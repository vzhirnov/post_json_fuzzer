import uuid

import collections.abc

from src.data_structures.test_method import TestMethod as tm


def extract_here(lst: list):
    return lst


class Fuzzy:
    def __init__(
        self,
        default_value,
        data_set: tuple,
        test_method=tm.pair_wise,
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
        lst = []
        for item in self.data_set:
            if isinstance(item, collections.Hashable):
                s.add(item)
            else:
                lst.append(item)
        return lst + list(s)

    def __repr__(self):
        return f"Fuzzy({self.default_value})-{self.obj_id[:6]}"

    def __hash__(self):
        return hash((self.obj_id, self.default_value))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.obj_id == other.obj_id

import random

class Fuzzy:

    def __init__(self, default_value, scenario: tuple):
        self.default_value = default_value
        self.scenario = tuple([default_value]) + scenario

        self.id = random.randrange(100, 10000000)

    def __repr__(self):
        return f'Fuzzy({self.default_value})-{id(self)}'

    def __hash__(self):
        return hash((self.default_value, self.scenario))

    def __eq__(self, other):
        return isinstance(other, Fuzzy) and self.id == other.id

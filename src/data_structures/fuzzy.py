import uuid


class Fuzzy:

    def __init__(self, default_value, scenario: tuple):
        self.default_value = default_value
        self.scenario = tuple([default_value]) + scenario

        self.obj_id = str(uuid.uuid4())

    def __repr__(self):
        return f'Fuzzy({self.default_value})-{self.obj_id[:6]}'

    def __hash__(self):
        return hash((self.obj_id, self.default_value, self.scenario))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.obj_id == other.obj_id

import enum


@enum.unique
class TestMethod(enum.Enum):
    hypothesis = 6
    pair_wise = 5
    triple_wise = 4
    combinations = 3
    take_curr_and_others_by_def = 2
    check_once_with_defaults = 1

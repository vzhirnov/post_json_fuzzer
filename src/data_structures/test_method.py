import enum


@enum.unique
class TestMethod(enum.Enum):
    pair_wise = 10
    miss_it = 9
    duplicate_it = 8
    nothing_more_but_this = 7
    hypothesis = 6  # ?
    pairs = 5
    triples = 4
    combinations = 3
    take_curr_and_others_by_def = 2
    check_once_with_defaults = 1

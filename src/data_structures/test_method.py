import enum


@enum.unique
class TestMethod(enum.Enum):
    miss_it = 9
    add_several_times = 8
    nothing_more_but_this = 7
    hypothesis = 6  # ?
    pair_wise = 5
    triple_wise = 4
    combinations = 3
    take_curr_and_others_by_def = 2
    check_once_with_defaults = 1

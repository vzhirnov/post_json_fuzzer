import enum


@enum.unique
class TestMethod(enum.Enum):  # TODO make aliasas for several values e.g. (pair_wise | miss_it) - need to?
    pair_wise = 7  # DONE: real pair_wise
    combinations = 6  # DONE: make all combinations

    take_curr_and_others_by_def = 5  # DONE
    # TODO: make test bundle with only this item to be mutated, and no other items at all in json
    nothing_more_but_this = 4

    # TODO: if key - make one case where this param is missed,
    #  if value - make it None. Ot try to bind key to value/vaue to key and make both be missed
    miss_it = 3
    duplicate_it = 2  # TODO: try to bind key and value and make them be missed

    hypothesis = 1    # TODO: description WIP

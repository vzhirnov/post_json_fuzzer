import enum


@enum.unique
class TestMethod(enum.Enum):  # TODO make aliasas for several values e.g. (pair_wise | miss_it) - need to?
    pair_wise = 1  # DONE: real pair_wise
    take_curr_and_others_by_def = 2  # TODO

    # TODO: if key - make one case where this param is missed,
    #  if value - make it None. Ot try to bind key to value/vaue to key and make both be missed
    miss_it = 3
    duplicate_it = 4  # TODO: try to bind key and value and make them be missed

    pairs = 5  # TODO: make all pairs, combinations from n by 2
    triples = 6  # TODO: make all triples, combinations from n by 3
    combinations = 7  # DONE: make all combinations

    hypothesis = 8    # TODO: description WIP
    # TODO: make test bundle with only this item to be mutated, and no other items at all in json
    nothing_more_but_this = 9

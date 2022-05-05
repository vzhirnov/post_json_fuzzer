from allpairspy import AllPairs

from itertools import combinations, product
from src.data_structures.test_method import TestMethod as tm


class Combinator:
    def __init__(self):
        pass

    def make_pair_wise(self, scenario: list) -> list:  # Correct
        return [values for values in AllPairs(scenario)]

    def make_all_combinations(self, scenario: list) -> list:   # Correct
        return list(product(*scenario))

    def make_n_wises(self, scenario: list, n: int) -> list:
        pass

    def make_all_pairs(self, scenario: list) -> list:
        pass

    def make_all_triplets(self, scenario: list) -> list:
        pass

    def miss_it(self, scenario: list) -> list:
        pass

    def duplicate_it(self, scenario: list) -> list:
        pass

    def nothing_more_but_this(self, scenario: list) -> list:
        pass

    def hypothesis(self, scenario: list) -> list:
        pass

    def take_curr_and_others_by_def(self, scenario: list) -> list:
        pass

    def check_once_with_defaults(self, scenario: list) -> list:
        pass

    def make_variants(self, scenario: list, test_method: tm):
        return {
            tm.pair_wise: self.make_pair_wise(scenario),  # Correct
            tm.pairs: self.make_all_pairs(scenario),
            tm.triples: self.make_all_triplets(scenario),
            tm.combinations: self.make_all_combinations(scenario),  # Correct

            tm.miss_it: self.miss_it(scenario),
            tm.duplicate_it: self.duplicate_it(scenario),
            tm.nothing_more_but_this: self.nothing_more_but_this(scenario),
            tm.hypothesis: self.hypothesis(scenario),
            tm.take_curr_and_others_by_def: self.take_curr_and_others_by_def(scenario),
        }.get(test_method, tm.pair_wise)


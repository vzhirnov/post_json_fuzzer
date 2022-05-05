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

    def make_variants(self, scenario: list, test_method: tm):
        return {
            tm.pair_wise: self.make_pair_wise(scenario),  # Correct
            tm.pairs: self.make_all_pairs(scenario),
            tm.triples: self.make_all_triplets(scenario),
            tm.combinations: self.make_all_combinations(scenario)  # Correct
        }.get(test_method, tm.pair_wise)


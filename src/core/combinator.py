from itertools import combinations, product

from src.data_structures.test_method import TestMethod as tm


class Combinator:
    def __init__(self):
        pass

    def make_n_wises(self, *scenario: list, n: int) -> list:
        res = list()

        def n_wises(*scenario: list):
            for t in combinations(scenario, n):
                for pair in product(*t):
                    yield pair

        for pair in n_wises(*scenario):
            res.append(pair)
        return res

    def make_pairs(self, *scenario: list) -> list:
        return self.make_n_wises(*scenario, n=2)

    def make_triplets(self, *scenario: list) -> list:
        return self.make_n_wises(*scenario, n=3)

    def make_combinations(self, *scenario: list) -> list:
        return list(product(*scenario))

    def make_variants(self, *scenario: list, test_method: tm):
        return {
            tm.pair_wise: self.make_pairs(*scenario),
            tm.triple_wise: self.make_triplets(*scenario),
            tm.combinations: self.make_combinations(*scenario)
        }.get(test_method, tm.pair_wise)


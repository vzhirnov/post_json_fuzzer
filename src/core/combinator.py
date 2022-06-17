from allpairspy import AllPairs

from itertools import product
from src.data_structures.test_method import TestMethod as tm


class Combinator:
    def __init__(self):
        pass

    def make_pair_wise(self, scenario: list) -> list:  # Correct
        res = [values for values in AllPairs(scenario)]
        return res

    def make_all_combinations(self, scenario: list) -> list:  # Correct
        res = list(product(*scenario))
        return res

    def miss_it(self, scenario: list) -> list:
        pass

    def duplicate_it(self, scenario: list) -> list:
        pass

    def nothing_more_but_this(self, scenario: list) -> list:
        pass

    def hypothesis(self, scenario: list) -> list:
        pass

    def take_curr_and_others_by_def(self, scenario: list) -> list:  # Correct
        res = []
        for md_tapes in scenario:
            for md_item in md_tapes:
                res.append(md_item)
        return res

    def check_once_with_defaults(self, scenario: list) -> list:
        pass

    def make_variants(self, scenario: list, test_method: tm):
        if test_method == tm.pair_wise:
            return (self.make_pair_wise(scenario),)  # Correct
        elif test_method == tm.combinations:
            return (self.make_all_combinations(scenario),)  # Correct
        elif test_method == tm.miss_it:
            return (self.miss_it(scenario),)
        elif test_method == tm.duplicate_it:
            return (self.duplicate_it(scenario),)
        elif test_method == tm.nothing_more_but_this:
            return (self.nothing_more_but_this(scenario),)
        elif test_method == tm.hypothesis:
            return (self.hypothesis(scenario),)
        elif test_method == tm.take_curr_and_others_by_def:  # Correct
            return (self.take_curr_and_others_by_def(scenario),)

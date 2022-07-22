from allpairspy import AllPairs

from itertools import product
from copy import deepcopy
from src.datastructures.testmethod import TestMethod as tm
from src.datastructures.metadata import Metadata

class Combinator:
    def __init__(self, scenario: dict, default_json_body=None):
        self.scenario = deepcopy(scenario)
        self.default_json_body = default_json_body if default_json_body else {}

    def take_curr_and_others_by_their_test_method(self):
        curr = []
        others = []
        for test_method, metadata_bundle in self.scenario.items():
            if test_method == tm.TAKE_CURR_AND_OTHERS_BY_THEIR_TEST_METHOD:
                for item in metadata_bundle:
                    curr += item
            else:
                others += self.make_variants(test_method=test_method)
        res = []
        for currs_metadata in curr:
            for others_metadata in others:
                for item in others_metadata:
                    res.append(
                        [currs_metadata] + [item]
                    )
        return res

    def make_pair_wise(self, scenario: list) -> list:  # Correct
        res = [values for values in AllPairs(scenario)]
        return res

    def make_all_combinations(self, scenario: list) -> list:  # Correct
        res = list(product(*scenario))
        return res

    def miss_it(self, scenario: list) -> list:
        res = []
        scen_copy = deepcopy(scenario)
        for md_tapes in scen_copy:
            for md_item in md_tapes:
                md_item.reset()
                res.append(md_item)
                break
        return res

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

    def add_once_with_defaults(self, scenario: list) -> list:
        pass

    def make_variants(self, test_method: tm):
        metadata_bundle = self.scenario[test_method]
        if test_method == tm.TAKE_CURR_AND_OTHERS_BY_THEIR_TEST_METHOD:
            return (self.take_curr_and_others_by_their_test_method(),)  # Correct
        if test_method == tm.PAIR_WISE:
            return (self.make_pair_wise(metadata_bundle),)  # Correct
        elif test_method == tm.COMBINATIONS:
            return (self.make_all_combinations(metadata_bundle),)  # Correct
        elif test_method == tm.MISS_IT:
            return (self.miss_it(metadata_bundle),)
        elif test_method == tm.DUPLICATE_IT:
            return (self.duplicate_it(metadata_bundle),)
        elif test_method == tm.NOTHING_MORE_BUT_THIS:
            return (self.nothing_more_but_this(metadata_bundle),)
        elif test_method == tm.HYPOTHESIS:
            return (self.hypothesis(metadata_bundle),)
        elif test_method == tm.TAKE_CURR_AND_OTHERS_BY_DEF:  # Correct
            return (self.take_curr_and_others_by_def(metadata_bundle),)

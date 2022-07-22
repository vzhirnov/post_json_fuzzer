import pytest

from src.datastructures.fuzzy import Fuzzy
from src.utils.handlers.dicts import *
from src.datastructures.testmethod import TestMethod as tm


class TestDicts:

    fuzzy = Fuzzy(
                    default_value="point",
                    suspicious_responses=[403, 200],
                    data_set=([], [[]],),
                    test_methods=tm.TAKE_CURR_AND_OTHERS_BY_DEF,
            )

    @pytest.mark.parametrize(
        "base_dict, fuzzy, expected_result",
        [
            (
                {
                    fuzzy: '1',
                    '2': 2,
                    '3': 3
                },
                fuzzy,
                [fuzzy.get_itself()]
            ),

            (
                    {
                        '1': {fuzzy: 1},
                        '2': 2,
                        '3': 3
                    },
                    fuzzy,
                    ['1', fuzzy.get_itself()]
            ),

            (
                    {
                        '1': {'4': [{fuzzy: 1}]},
                        '2': 2,
                        '3': 3
                    },
                    fuzzy,
                    ['1', '4', 0, fuzzy.get_itself()]
            ),

            (
                    {
                        '1': {'4': [{'5': [{fuzzy: 6}]}]},
                        '2': 2,
                        '3': 3
                    },
                    fuzzy,
                    ['1', '4', 0, '5', 0, fuzzy.get_itself()]
            ),
        ],
    )
    def test_find_path_for_key(self, base_dict, fuzzy, expected_result):
        find_path_for_key(base_dict, fuzzy)
        path_to_curr_deep_key = result.pop()
        assert path_to_curr_deep_key == expected_result

    @pytest.mark.parametrize(
        "base_dict, fuzzy, expected_result",
        [
            (
                {
                    '1': fuzzy,
                    '2': 2,
                    '3': 3
                },
                fuzzy,
                ['1']
            ),

            (
                    {
                        '1': {1: fuzzy},
                        '2': 2,
                        '3': 3
                    },
                    fuzzy,
                    ['1', 1]
            ),

            (
                    {
                        '1': {'4': [{1: fuzzy}]},
                        '2': 2,
                        '3': 3
                    },
                    fuzzy,
                    ['1', '4', 0, 1]
            ),

            (
                    {
                        '1': {'4': [{'5': [{6: fuzzy}]}]},
                        '2': 2,
                        '3': 3
                    },
                    fuzzy,
                    ['1', '4', 0, '5', 0, 6]
            ),
        ],
    )
    def test_find_path_for_value(self, base_dict, fuzzy, expected_result):
        find_path_for_value(base_dict, fuzzy)
        path_to_curr_deep_key = result.pop()
        assert path_to_curr_deep_key == expected_result


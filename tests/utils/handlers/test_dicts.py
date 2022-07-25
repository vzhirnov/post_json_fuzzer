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

    @pytest.mark.parametrize(
        "base_dct, expected_result",
        [
            ({'b': 2, 'a': 1}, {'a': 1, 'b': 2}),
            ({'b': 2, 'a': {'e': 4, 'd': 3}}, {'a': {'d': 3, 'e': 4}, 'b': 2}),
        ]
    )
    def test_seep_sorted_dicts(self, base_dct, expected_result):
        srt_dct = deep_sorted(base_dct)
        assert str(srt_dct) == str(expected_result)

    @pytest.mark.parametrize(
        "base_lst, expected_result",
        [
            (["b", "a"], ["a", "b"]),
            (["b", "a", "d", "c"], ["a", "b", "c", "d"]),
            (["b", "a", ["d", "c"]], [['c', 'd'], 'a', 'b']),

            (
                    {'b': 2, 'a': ["d", "c", {"b": {'f': 3, 'e': 4}, 'a': 1}]},
                    {'a': ['c', 'd', {'a': 1, 'b': {'f': 3, 'e': 4}}], 'b': 2}
            ),
            (
                {
                    'c': ['2', 1, [4, 3, 9, 11, {'b': 1, 'a': 2}], [5, 6, 7, 3, 2, {'1': 1, '2': 2, '3': 3, '4': 4}]],
                    'z': 2, 1: 1
                },
                {
                    1: 1,
                    'c': [1, '2', [11, 3, 4, 9, {'a': 2, 'b': 1}], [2, 3, 5, 6, 7, {'1': 1, '2': 2, '3': 3, '4': 4}]],
                    'z': 2
                }
            ),
        ]
    )
    def test_seep_sorted_lists(self, base_lst, expected_result):
        base_lst = deep_sorted(base_lst)
        assert str(base_lst) == str(expected_result)

    @pytest.mark.parametrize(
        "base_dct, expected_result",
        [
            (
                [
                    {'offset': '+0', 'limit': 100, 'filter': {'clientid': [132]}},
                    {'offset': '+0', 'limit': 100, 'filter': {'clientid': [132]}}
                ],
                [{'filter': {'clientid': [132]}, 'limit': 100, 'offset': '+0'}]
            )
        ]
    )
    def test_make_dictionary_items_unique(self, base_dct, expected_result):
        base_lst = make_dictionary_items_unique(base_dct)
        assert str(base_lst) == str(expected_result)

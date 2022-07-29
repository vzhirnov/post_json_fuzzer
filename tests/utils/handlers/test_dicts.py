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
            ({fuzzy: "1", "2": 2, "3": 3}, fuzzy, [fuzzy.get_itself()]),
            ({"1": {fuzzy: 1}, "2": 2, "3": 3}, fuzzy, ["1", fuzzy.get_itself()]),
            (
                    {"1": {"4": [{fuzzy: 1}]}, "2": 2, "3": 3},
                    fuzzy,
                    ["1", "4", 0, fuzzy.get_itself()],
            ),
            (
                    {"1": {"4": [{"5": [{fuzzy: 6}]}]}, "2": 2, "3": 3},
                    fuzzy,
                    ["1", "4", 0, "5", 0, fuzzy.get_itself()],
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
            ({"1": fuzzy, "2": 2, "3": 3}, fuzzy, ["1"]),
            ({"1": {1: fuzzy}, "2": 2, "3": 3}, fuzzy, ["1", 1]),
            ({"1": {"4": [{1: fuzzy}]}, "2": 2, "3": 3}, fuzzy, ["1", "4", 0, 1]),
            (
                    {"1": {"4": [{"5": [{6: fuzzy}]}]}, "2": 2, "3": 3},
                    fuzzy,
                    ["1", "4", 0, "5", 0, 6],
            ),
            (
                    {'1': [fuzzy, 'other_str']},
                    fuzzy,
                    ['1', 0]
            ),
            (
                    {'1': [[fuzzy, 'other_str']]},
                    fuzzy,
                    ['1', 0, 0]
            ),
            (
                    {'1': {2: [fuzzy, 'other_str']}},
                    fuzzy,
                    ['1', 2, 0]
            ),
        ],
    )
    def test_find_path_for_value(self, base_dict, fuzzy, expected_result):
        find_path_for_value(base_dict, fuzzy)
        path_to_curr_deep_key = result.pop()
        result.clear()
        path.clear()
        assert path_to_curr_deep_key == expected_result

    @pytest.mark.parametrize(
        "base_dct, expected_result",
        [
            ({"b": 2, "a": 1}, {"a": 1, "b": 2}),
            ({"b": 2, "a": {"e": 4, "d": 3}}, {"a": {"d": 3, "e": 4}, "b": 2}),
        ],
    )
    def test_seep_sorted_dicts(self, base_dct, expected_result):
        srt_dct = deep_sorted(base_dct)
        assert str(srt_dct) == str(expected_result)

    @pytest.mark.parametrize(
        "base_lst, expected_result",
        [
            (["b", "a"], ["a", "b"]),
            (["b", "a", "d", "c"], ["a", "b", "c", "d"]),
            (["b", "a", ["d", "c"]], [["c", "d"], "a", "b"]),
            (
                    {"b": 2, "a": ["d", "c", {"b": {"f": 3, "e": 4}, "a": 1}]},
                    {"a": ["c", "d", {"a": 1, "b": {"f": 3, "e": 4}}], "b": 2},
            ),
            (
                    {
                        "c": [
                            "2",
                            1,
                            [4, 3, 9, 11, {"b": 1, "a": 2}],
                            [5, 6, 7, 3, 2, {"1": 1, "2": 2, "3": 3, "4": 4}],
                        ],
                        "z": 2,
                        1: 1,
                    },
                    {
                        1: 1,
                        "c": [
                            1,
                            "2",
                            [11, 3, 4, 9, {"a": 2, "b": 1}],
                            [2, 3, 5, 6, 7, {"1": 1, "2": 2, "3": 3, "4": 4}],
                        ],
                        "z": 2,
                    },
            ),
        ],
    )
    def test_seep_sorted_lists(self, base_lst, expected_result):
        base_lst = deep_sorted(base_lst)
        assert str(base_lst) == str(expected_result)

    @pytest.mark.parametrize(
        "base_dct, expected_result",
        [
            (
                    [
                        {"offset": "+0", "limit": 100, "filter": {"clientid": [132]}},
                        {"offset": "+0", "limit": 100, "filter": {"clientid": [132]}},
                    ],
                    [{"filter": {"clientid": [132]}, "limit": 100, "offset": "+0"}],
            )
        ],
    )
    def test_make_dictionary_items_unique(self, base_dct, expected_result):
        base_lst = make_dictionary_items_unique(base_dct)
        assert str(base_lst) == str(expected_result)

    @pytest.mark.parametrize(
        "base_dict, fuzzy, expected_result",
        [
            ({fuzzy: "1", "2": 2, "3": 3}, fuzzy, ([fuzzy.get_itself()], 0),),
            ({"1": {fuzzy: 1}, "2": 2, "3": 3}, fuzzy, (["1", fuzzy.get_itself()], 0),),
            (
                    {"1": {"4": [{fuzzy: 1}]}, "2": 2, "3": 3},
                    fuzzy,
                    (["1", "4", 0, fuzzy.get_itself()], 0),
            ),
            (
                    {"1": {"4": [{"5": [{fuzzy: 6}]}]}, "2": 2, "3": 3},
                    fuzzy,
                    (["1", "4", 0, "5", 0, fuzzy.get_itself()], 0),
            ),
        ],
    )
    def test_find_key_in_dlcontainer(self, base_dict, fuzzy, expected_result):
        dl_containner = DLContainer(base_dict)
        res, key_or_val = dl_containner.get(fuzzy, None)
        assert (res, key_or_val) == expected_result

    @pytest.mark.parametrize(
        "base_dict, fuzzy, new_value, expected_result",
        [
            (
                    {4: {fuzzy: "1", "2": 2, "3": 3}},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({4: {'7a172f8d-6f6f-4f85-af3c-8ef24a871ec4': "1", "2": 2, "3": 3}}, 0),
            ),

            (
                    {4: {fuzzy: "1", "2": 2, "3": 3}},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({4: {'7a172f8d-6f6f-4f85-af3c-8ef24a871ec4': "1", "2": 2, "3": 3}}, 0),
            ),
            (
                    {"1": {fuzzy: 1}, "2": 2, "3": 3},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': {'7a172f8d-6f6f-4f85-af3c-8ef24a871ec4': 1}, '2': 2, '3': 3}, 0),
            ),
            (
                    {"1": {"4": [{fuzzy: 1}]}, "2": 2, "3": 3},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': {'4': [{'7a172f8d-6f6f-4f85-af3c-8ef24a871ec4': 1}]}, '2': 2, '3': 3}, 0),
            ),
            (
                    {"1": {"4": [{"5": [{fuzzy: 6}]}]}, "2": 2, "3": 3},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': {'4': [{'5': [{'7a172f8d-6f6f-4f85-af3c-8ef24a871ec4': 6}]}]}, '2': 2, '3': 3}, 0),
            ),
        ],
    )
    def test_find_and_update_key_in_dlcontainer(self, base_dict, fuzzy, new_value, expected_result):
        dl_containner = DLContainer(base_dict)
        path_to_item, key_or_value = dl_containner.get(fuzzy, None)
        dl_containner.update_item(path_to_item, new_value, key_or_value)
        assert (dl_containner.base_object, key_or_value) == expected_result

    @pytest.mark.parametrize(
        "base_dict, fuzzy, expected_result",
        [
            ({"1": fuzzy, "2": 2, "3": 3}, fuzzy, (["1"], 1)),
            ({"1": {1: fuzzy}, "2": 2, "3": 3}, fuzzy, (["1", 1], 1)),
            ({"1": {"4": [{1: fuzzy}]}, "2": 2, "3": 3}, fuzzy, (["1", "4", 0, 1], 1)),
            (
                    {"1": {"4": [{"5": [{6: fuzzy}]}]}, "2": 2, "3": 3},
                    fuzzy,
                    (["1", "4", 0, "5", 0, 6], 1)
            ),
            (
                    {'1': [fuzzy, 'other_str']},
                    fuzzy,
                    (['1', 0], 1)
            ),
            (
                    {'1': [[fuzzy, 'other_str']]},
                    fuzzy,
                    (['1', 0, 0], 1)
            ),
            (
                    {'1': {2: [fuzzy, 'other_str']}},
                    fuzzy,
                    (['1', 2, 0], 1)
            ),
            (
                    {'1': {2: [fuzzy, 'other_str']}},
                    "fuzzy",
                    (None, None)
            ),
        ],
    )
    def test_find_value_in_dlcontainer(self, base_dict, fuzzy, expected_result):
        dl_containner = DLContainer(base_dict)
        res, key_or_value = dl_containner.get(fuzzy, None)
        assert (res, key_or_value) == expected_result

    @pytest.mark.parametrize(
        "base_dict, fuzzy, new_value, expected_result",
        [
            (
                    {"1": fuzzy, "2": 2, "3": 3},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4', '2': 2, '3': 3}, 1)
            ),
            (
                    {"1": {1: fuzzy}, "2": 2, "3": 3},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': {1: '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4'}, '2': 2, '3': 3}, 1)
            ),
            (
                    {"1": {"4": [{1: fuzzy}]}, "2": 2, "3": 3},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({"1": {"4": [{1: '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4'}]}, "2": 2, "3": 3}, 1)
            ),
            (
                    {"1": {"4": [{"5": [{6: fuzzy}]}]}, "2": 2, "3": 3},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({"1": {"4": [{"5": [{6: '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4'}]}]}, "2": 2, "3": 3}, 1),
            ),
            (
                    {'1': [fuzzy, 'other_str']},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': ['7a172f8d-6f6f-4f85-af3c-8ef24a871ec4', 'other_str']}, 1)
            ),
            (
                    {'1': [[fuzzy, 'other_str']]},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': [['7a172f8d-6f6f-4f85-af3c-8ef24a871ec4', 'other_str']]}, 1)
            ),
            (
                    {'1': {2: [fuzzy, 'other_str']}},
                    fuzzy,
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': {2: ['7a172f8d-6f6f-4f85-af3c-8ef24a871ec4', 'other_str']}}, 1)
            ),
            (
                    {'1': {2: [fuzzy, 'other_str']}},
                    "fuzzy",
                    '7a172f8d-6f6f-4f85-af3c-8ef24a871ec4',
                    ({'1': {2: [fuzzy, 'other_str']}}, None)
            ),
        ],
    )
    def test_find_and_update_value_in_dlcontainer(self, base_dict, fuzzy, new_value, expected_result):
        dl_containner = DLContainer(base_dict)
        path_to_item, key_or_value = dl_containner.get(fuzzy, None)
        dl_containner.update_item(path_to_item, new_value, key_or_value)
        assert (dl_containner.base_object, key_or_value) == expected_result

import random
import ast
import pytest
import pyradamsa

from collections.abc import Iterable

from src.utils.parser.generate import generate_strategy
from src.strategies.strategies import register_strategy, register_method
from src.utils.strategy.modifiers import list_once, list_several_times

digits = [1, 2, 3, 0.01]
strings = ['4', '5', '6']
different_elems = [1, '2', 3.03, (4, ), {5: 5}, [6], False, None, range(7)]


bls = [True, False]

register_strategy('digits', digits)
register_strategy('strings', strings)
register_strategy('different_elems', different_elems)
register_strategy('bls', bls)


def nullify_all_elements(items):
    return [0] * len(items)


def mutate_by_radamsa(item):
    rad = pyradamsa.Radamsa()
    fuzzed_item = rad.fuzz(bytes(str(item), 'utf-8'), seed=random.randrange(2000))
    try:
        decoded_item = fuzzed_item.decode()
        return decoded_item
    except Exception:
        return fuzzed_item


def mutate_all_elements_by_radamsa(items):
    res = []
    if isinstance(items, Iterable):
        items_types = [type(x) for x in items]
        mutated_items = [mutate_by_radamsa(x) for x in items]
        for i, item in enumerate(mutated_items):
            try:
                elem = items_types[i](item)
                res.append(elem)
            except Exception:
                res.append(item)
        return res
    return mutate_by_radamsa(items)


register_method('nullify_all_elements', nullify_all_elements)
register_method('mutate_all_elements_by_radamsa', mutate_all_elements_by_radamsa)

register_method('list_once', list_once)
register_method('list_several_times', list_several_times)


@pytest.mark.parametrize(
    "pattern, expected_result",
    [
        ((1,), [1]),
        (("1",), ["1"]),
        (("www.test.com",), ["www.test.com"]),
        ((True,), [True]),
        ((None,), [None]),
        (([1],), [[1]]),
        ((["test"],), [["test"]]),
        (([["test"]],), [[["test"]]]),
        (([True],), [[True]]),

        (([1, 2],), [[1, 2]]),

        (([1], 2), [[1], 2]),
        (("1", 2), ["1", 2]),
        ((["1"], 2), [["1"], 2]),
        ((True, False), [True, False]),
        (([True, False],), [[True, False]]),


        ((1, 2, 3), [1, 2, 3]),
        ((1, 2, [3]), [1, 2, [3]]),
        (([1], [2], [3]), [[1], [2], [3]]),
        (('1', '2', '3'), ['1', '2', '3']),


        ((1, 2, '+'), [[2, 1]]),
        (([1], 2, '+',), [[1, 2]]),
        (("1", 2, '+'), [[2, "1"]]),
        ((True, "False", '+'), [["False", True]]),

        (([1], [2], '+'), [[2, [1]]]),


        (('#ADD_DATASET#GET#digits$', '@'), digits),
        (('#ADD_DATASET #GET#digits$', '@'), digits),
        (('#ADD_DATASET#GET #digits$', '@'), digits),
        (('#ADD_DATASET #GET #digits$', '@'), digits),  # TODO make it possible as '#ADD_DATASET #GET #digits$'

        ((1, '#ADD_DATASET#GET#digits$', '+', '@'), [1, 2, 3, 0.01, 1]),

        (("1", [4, 5, 6], '+', '@'), [4, 5, 6, '1']),
        (("1", '#ADD_DATASET#GET#strings$', '+', '@'), ['4', '5', '6', '1']),
        ((0, '#ADD_DATASET#GET#bls$', '+', '@'), [True, False, 0]),


        ((1, '#APPLY#LIST_IT#list_once$'), [[1]]),
        ((1, '#APPLY #LIST_IT#list_once$'), [[1]]),
        ((1, '#APPLY#LIST_IT #list_once$'), [[1]]),
        ((1, '#APPLY #LIST_IT #list_once$'), [[1]]),

        ((1, '#APPLY#LIST_IT#list_several_times#2$'), [[[1]]]),
        (('#ADD_DATASET#GET#strings$', '#APPLY#MUTATE_IT#nullify_all_elements$', '@'), [0, 0, 0]),
    ]
)
def test_generate_strategy(pattern, expected_result):
    assert generate_strategy(pattern) == expected_result


@pytest.mark.parametrize(
    "pattern, expected_result",
    [
        (('#ADD_DATASET#GET#different_elems$', '#FUNC#MUTATE_IT#mutate_all_elements_by_radamsa$', '@'), strings),
    ]
)
def test_mutators(pattern, expected_result):
    assert generate_strategy(pattern) != expected_result

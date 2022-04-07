import pytest

from src.utils.parser.generate import generate_strategy
from src.strategies.strategies import register_strategy, register_method
from src.utils.strategy.modifiers import list_once, list_several_times

digits = [1, 2, 3, 0.01]
strings = ['4', '5', '6']
bls = [True, False]

register_strategy('digits', digits)
register_strategy('strings', strings)
register_strategy('bls', bls)


def nullify_all_elements(items):
    return [0] * len(items)


register_method('nullify_all_elements', nullify_all_elements)

register_method('list_once', list_once)
register_method('list_several_times', list_several_times)


@pytest.mark.parametrize(
    "pattern, expected_result",
    [
        (('#STRATEGY#digits$',), digits),  # TODO get rid of ','
        ((1, '#STRATEGY#digits$', '+'), [1, 2, 3, 0.01, 1]),

        (("1", '#STRATEGY#strings$', '+'), ['4', '5', '6', '1']),
        ((0, '#STRATEGY#bls$', '+'), [True, False, 0]),


        ((1, '#FUNC#LIST_IT#list_once$'), [[1]]),
        ((1, '#FUNC#LIST_IT#list_several_times#2$'), [[[1]]]),
        (('#STRATEGY#strings$', '#FUNC#MUTATE_IT#nullify_all_elements$'), [0, 0, 0]),

        ((1, 2, 3), [1, 2, 3]),
        (([1],), [[1]]),  # TODO: bug: works only with , check regexes
        ((["test"],), [["test"]]),

        (([1], 2), [[1], 2]),
        ((1, 2, [3]), [1, 2, [3]]),
        (([1], [2], [3]), [[1], [2], [3]]),
        (('1', '2', '3'), ['1', '2', '3']),
        ((True, False), [True, False]),
        ([True, False], [True, False]),

        ((1, 2, '+'), [2, 1]),
        ((True, "False", '+'), ["False", True]),

        (([1], [2], '|'), [2, 1]),
        (([True], [2], '|'), [2, True]),
    ]
)
def test_generate_strategy(pattern, expected_result):
    assert generate_strategy(pattern) == expected_result

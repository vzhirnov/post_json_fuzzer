import pytest

from src.core.parser.generate import generate_strategy
from src.strategies.registrars import register_strategy, register_method, register_generator
from src.strategies.methods import list_once, list_several_times, mutate_all_elements_by_radamsa
from  src.strategies.generators import rand_nums_in_range

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


register_method('nullify_all_elements', nullify_all_elements)
register_method('mutate_all_elements_by_radamsa', mutate_all_elements_by_radamsa)

register_method('list_once', list_once)
register_method('list_several_times', list_several_times)

register_generator('rand_nums_in_range', rand_nums_in_range)


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
    ]
)
def test_generate_strategy(pattern, expected_result) -> None:
    """
    This test checks if adding simple object to stack handles by DSL as expected
    :param pattern: string with simple DSL code
    :param expected_result: result list of elements after DSL has made its work
    :return: None
    """
    assert generate_strategy(pattern) == expected_result


@pytest.mark.parametrize(
    "pattern, expected_result",
    [
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
def test_generate_strategy(pattern, expected_result) -> None:
    """
    This test checks if complex DSL code generates the correct result lists
    :param pattern: string with complex DSL code
    :param expected_result: result list of elements after DSL has made its work
    :return: None
    """
    assert generate_strategy(pattern) == expected_result


@pytest.mark.parametrize(
    "pattern, expected_result",
    [
        (('#ADD_DATASET#GET#different_elems$', '#FUNC#MUTATE_IT#mutate_all_elements_by_radamsa$', '@'), []),
    ]
)
def test_mutators(pattern, expected_result) -> None:
    """
    This test check results lists made by mutators
    :param pattern: string with complex DSL code
    :param expected_result: result list of elements after DSL has made its work
    :return: None
    """
    assert generate_strategy(pattern) != expected_result


@pytest.mark.parametrize(
    "pattern, expected_result",
    [
        (('#ADD_DATASET#GENERATE#rand_nums_in_range#0#10$', '@'), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
    ]
)
def test_generators(pattern, expected_result) -> None:
    """
    This test check results lists made by generators
    :param pattern: string with complex DSL code
    :param expected_result: result list of elements after DSL has made its work
    :return: None
    """
    assert generate_strategy(pattern) == expected_result

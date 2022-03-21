from src.utils.strategy.modifiers import restore_data_type, list_current_items, unlist_current_items
from src.utils.parser.view import parser_view
from src.data_structures.datastructures import Stack
from src.strategies.strategies import STRATEGY_1, STRATEGY_2, STAR


def generate_strategy(strategy_info):
    # TODO: migrate assert upper where it is really required
    # assert isinstance(strategy_info, str)  # and all(x not in strategy_info for x in ['(', ')'])
    # TODO: add asserts:
    # TODO: num of opened [s is equal to ]s
    strategy = parser_view(str(strategy_info))
    strategy = restore_data_type(strategy)
    stack = Stack()
    result_strategy = []
    for item in strategy:
        if item == 'STRATEGY_1':
            elem = stack.pop()
            result_strategy.insert(0, elem)
            result_strategy += STRATEGY_1
            stack.push(result_strategy)
            result_strategy = []
        elif item == 'STRATEGY_2':
            elem = stack.pop()
            result_strategy.insert(0, elem)
            result_strategy += STRATEGY_2
            stack.push(result_strategy)
            result_strategy = []
        elif item == 'STAR':
            elem = stack.pop()
            result_strategy.insert(0, elem)
            result_strategy += STAR
            stack.push(result_strategy)
            result_strategy = []
        elif item == '^':
            elem = stack.pop()
            if isinstance(elem, list):
                result_strategy = stack.pop()
                result_strategy = list_current_items(result_strategy)
                stack.push(result_strategy)
                result_strategy = []
        elif item == '+':
            elem1 = stack.pop()
            elem2 = stack.pop()
            result_strategy = elem1 + elem2
            stack.push(result_strategy)
            result_strategy = []
        else:
            stack.push(item)
    return unlist_current_items(stack.pop_all())


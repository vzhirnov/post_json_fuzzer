import ast

from src.utils.strategy.modifiers import restore_data_type, list_current_items, unlist_current_items, mutate
from src.utils.parser.view import parser_view
from src.data_structures.datastructures import Stack
from src.strategies.strategies import ready_strategies, strategy_methods


def sum_elems_of_different_types(elem1, elem2):
    if isinstance(elem1, list) and isinstance(elem2, list):
        elem1.append(elem2)
        return elem1
    if isinstance(elem1, list):
        elem1.append(elem2)
        return elem1
    elif isinstance(elem2, list):
        elem2.append(elem1)
        return elem2
    else:
        res = [elem1, elem2]
        return res


def get_last_part_after_pattern(base_line, pattern):
    return base_line.split(pattern, 1)[1]


def get_func_name_and_args_num(base_line, func, args):
    s1 = base_line.split(func, 1)[1]
    index = s1.find(args)
    func_name = s1[:index - 1]
    args_num = s1.split(args, 1)[1]
    return func_name, args_num


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
        if isinstance(item, str):
            if item.startswith('ADD_STRATEGY_'):
                strategy = get_last_part_after_pattern(item, 'ADD_STRATEGY_')
                result_strategy += ready_strategies[strategy]
                stack.push(result_strategy)
                result_strategy = []
            elif item.startswith('FUNC_'):
                func_name, args_num = get_func_name_and_args_num(item, 'FUNC_', 'ARGS_NUM_')
                lst = []
                for _ in range(0, ast.literal_eval(args_num)):
                    elem = stack.pop()
                    lst.append(elem)
                lst = lst[::-1]
                result_strategy = strategy_methods[func_name](*lst)
                stack.push(result_strategy)
                result_strategy = []
            elif item == 'MUTATE':
                elem = stack.pop()
                result_strategy = mutate(elem)
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
                result_strategy = sum_elems_of_different_types(elem1, elem2)
                stack.push(result_strategy)
                result_strategy = []
            elif item == '|':
                elem1 = stack.pop()
                elem2 = stack.pop()
                result_strategy = elem1 + elem2
                stack.push(result_strategy)
                result_strategy = []
            else:
                stack.push(item)
        else:
            stack.push(item)
    return unlist_current_items(stack.pop_all())


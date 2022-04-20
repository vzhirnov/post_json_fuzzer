import re

from src.strategies.methods import restore_data_type
from src.core.parser.view import parser_view
from src.data_structures.stack import Stack
from src.strategies.metadata_aggregator import data_sets, methods, generators
from src.utils.types_handler import restore_type


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


def unlist_current_item(item) -> tuple:
    pass


def get_last_part_after_pattern(base_line, pattern):
    index = base_line.find(pattern) + len(pattern)
    index += base_line[index:].find('#')
    return base_line[(index + 1):]


def extract_method_info(base_line, pattern):
    index = base_line.find(pattern) + len(pattern)
    return base_line[index::]


def get_seq_by_pattern_and_terminate_symb(base_line, pattern, term_sym='$'):
    term_index = base_line.find(term_sym)
    seq_start = base_line.find(pattern) + len(pattern)
    return base_line[seq_start:term_index]


def get_func_name_and_args(base_line, term_sym='$'):
    term_index = base_line.find(term_sym)
    res = re.split(r'[# ]+', base_line[:term_index])
    res = [x for x in res if x != '']
    return res[0], res[1:]


def save_type_info(tup: tuple):
    l = []
    for item in tup:
        if isinstance(item, str):
            if item.isdigit():
                l.append(item + '^s')
            elif item in ('True', 'False'):
                l.append(str(item) + '^b')
            else:
                l.append(item)
        else:
            l.append(item)
    return tuple(l)


def generate_strategy(strategy_info: tuple):
    assert \
        all(x.endswith('$') for x in strategy_info if isinstance(x, str) and x.startswith('#')), \
        'Invalid syntax. Have you installed all the # characters and the terminator symbol $?'
    strategy = parser_view(
        str(save_type_info(strategy_info))
    )  # TODO replace word strategy if there is an another meaning
    strategy = restore_data_type(strategy)
    stack = Stack()
    result_strategy = []
    for item in strategy:
        if isinstance(item, str):
            if item.startswith('#ADD_DATASET'):
                strategy = get_seq_by_pattern_and_terminate_symb(item, '#ADD_DATASET')
                if '#GET' in strategy:
                    strategy = get_last_part_after_pattern(strategy, '#GET')
                    result_strategy += data_sets[strategy]
                    stack.push(result_strategy)
                    result_strategy = []
                elif '#GENERATE' in strategy:
                    method_info = extract_method_info(item, '#GENERATE')
                    method_name, args = get_func_name_and_args(method_info)
                    method_name = generators[method_name]
                    result_strategy = method_name(*(restore_type(args)))
                    stack.push(result_strategy)
                    result_strategy = []
            elif item.startswith('#APPLY'):
                method_info = extract_method_info(item, '#APPLY')
                method_name, args = get_func_name_and_args(method_info)
                if method_name == 'MUTATE_IT':
                    elem = stack.pop()
                    nm = methods[args[0]]
                    result_strategy = nm(elem)
                    stack.push(result_strategy)
                    result_strategy = []
                elif method_name == 'LIST_IT':
                    elem = stack.pop()
                    nm = methods[args[0]]
                    result_strategy = nm(elem, *args[1:])
                    stack.push(result_strategy)
                    result_strategy = []
                elif method_name == 'ADD_BORDER_CASES':
                    nm = methods[method_name]
                    result_strategy = nm(*(restore_type(args)))
                    stack.push(result_strategy)
                    result_strategy = []
            elif item == '+':
                elem1 = stack.pop()
                elem2 = stack.pop()
                result_strategy = sum_elems_of_different_types(elem1, elem2)
                stack.push(result_strategy)
                result_strategy = []
            elif item == '@':
                return stack.pop()
            else:
                stack.push(item)
        else:
            stack.push(item)
    return stack.items

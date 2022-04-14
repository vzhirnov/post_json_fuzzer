import ast
import random
import pyradamsa

from collections.abc import Iterable


def restore_data_type(littered_data: list):
    l = []
    type_add_info = ["^s", "^b"]
    for littered_item in littered_data:
        try:
            c = ast.literal_eval(littered_item)
            l.append(c)
        except Exception:
            if littered_item.endswith(tuple(type_add_info)):
                index = littered_item.rfind("^")
                littered_item = littered_item[:index]
            l.append(littered_item)
    return l


def make_ast_literal_eval(item):
    return [ast.literal_eval(x) for x in item]


def mutate_by_radamsa(item):
    rad = pyradamsa.Radamsa()
    fuzzed_item = rad.fuzz(
        bytes(str(item), 'utf-8'), seed=random.randrange(2000)
    )
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


def add_border_cases(left_num: int, right_num: int):
    if not isinstance(left_num, int) or not isinstance(right_num, int):
        return [0]
    return list((
        left_num - 1, left_num, random.randrange(left_num + 1, right_num),
        right_num, right_num + 1
    ))

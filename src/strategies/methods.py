import random
import pyradamsa
import base64

from collections.abc import Iterable
from src.utils.types_handler import is_evaluable
from default_values import DefaultValues


def mutate_by_radamsa(item, seed=random.randrange(10000), max_num_of_mutations=random.randrange(1, 5)):
    rad = pyradamsa.Radamsa()
    fuzzed_item = rad.fuzz(bytes(str(item), "utf-8"), seed=seed, max_mut=max_num_of_mutations)
    try:
        decoded_item = fuzzed_item.decode()
        return decoded_item
    except Exception:
        return fuzzed_item


def mutate_all_by_radamsa(items):
    res = []
    if isinstance(items, Iterable):
        items_types = [type(x) for x in items]
        mutated_items = [mutate_by_radamsa(x) for x in items]
        for i, item in enumerate(mutated_items):
            try:
                elem = (
                    items_types[i](item)
                    if type(item) == items_types[i]
                    else base64.b64encode(item).decode("ascii")
                )
                res.append(elem)
            except Exception:
                res.append(item)
        return res
    return mutate_by_radamsa(items)


def add_border_cases(left_num: int, right_num: int) -> list:
    if not isinstance(left_num, int) or not isinstance(right_num, int):
        return [0]
    return list((left_num - 1, left_num, right_num, right_num + 1))


def add_from_file(file_name: str) -> list:
    res = []
    root_dir = DefaultValues.PROJECT_ROOT_DIR
    path_to_file = root_dir / file_name
    with open(path_to_file) as file:
        for line in file:
            l = line.rstrip()
            if is_evaluable(l):
                res.append(l)
            else:
                res.append(str(line))
    return res


def get_pack_by_methods(item, funcs: list):
    res = []
    for func in funcs:
        res.append(func(item))
    return res


def list_once(items):
    if isinstance(items, list):
        return [[i] for i in items]
    return [items]


def list_several_times(n=2):
    def list_it(items):
        lst = items
        for _ in range(n):
            lst = list_once(lst)
        return lst

    return list_it

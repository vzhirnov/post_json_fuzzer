import ast
import itertools
import re
import uuid

from src.utils.parser.generate import generate_strategy
from src.utils.strategy.modifiers import make_ast_literal_eval


def get_jsons_for_fuzzing(d_base):
    matched_items, d = get_interesting_data(d_base)
    experiments = get_all_combinations(matched_items)
    jsons = get_final_data(experiments, d)
    return jsons


def get_interesting_data(d_base):
    d = str(d_base)
    res = make_ast_literal_eval(re.findall(r'\(.*?\)', d))
    if not res:
        raise Exception("Error: no metadata to make a fuzzing decision")
    matched_items = dict()

    for index, item in enumerate(res):
        matched_index = str(uuid.uuid4())
        d = d.replace(str(item), matched_index)
        matched_items[matched_index] = item

    for key, value in matched_items.items():
        matched_items[key] = generate_strategy(value)

    return matched_items, d


def get_all_combinations(matched_items):
    keys, values = zip(*matched_items.items())  # TODO: assert if no ()s with strategy, just plain dict values
    experiments = [dict(zip(keys, v)) for v in itertools.product(*values)]
    return experiments


def get_final_data(experiments, d_base):
    result_jsons = []
    fuzz_item = dict()
    for dict_items in experiments:
        tmp_d = d_base
        for key, value in dict_items.items():
            if d_base[d_base.find(key) + len(key)] == ',':
                a = d_base[:d_base.find(key)].split('\'')[1::2][0]
                fuzz_item.update({a: value})
            elif d_base[d_base.find(key) + len(key)] == ':':
                b = d_base[(d_base.find(key) + len(key)):].split('\'')[1]
                fuzz_item.update({value: b})
            else:
                raise Exception("This should never happen!")
            tmp_d = tmp_d.replace(str(key), "'" + str(value) + "'" if isinstance(value, str) else str(value))
        res_dict = ast.literal_eval(tmp_d)
        result_jsons.append((res_dict, fuzz_item))
        fuzz_item = {}
    return result_jsons


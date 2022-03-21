import ast
import itertools
import re
import uuid

from src.utils.parser.generate import generate_strategy
from src.utils.strategy.modifiers import make_ast_literal_eval


def get_jsons_for_fuzzing(d_base):
    matched_items, d = get_data(d_base)
    experiments = make_all_permutations(matched_items)
    jsons = get_final_data(experiments, d)
    return jsons


def get_data(d_base):
    d = str(d_base)
    res = make_ast_literal_eval(re.findall(r'\(.*?\)', d))
    matched_items = dict()

    for index, item in enumerate(res):
        matched_index = str(uuid.uuid4())
        d = d.replace(str(item), matched_index)
        matched_items[matched_index] = item

    for key, value in matched_items.items():
        matched_items[key] = generate_strategy(value)

    return matched_items, d


def make_all_permutations(matched_items):
    keys, values = zip(*matched_items.items())  # TODO: assert if no ()s with strategy, just plain dict values
    experiments = [dict(zip(keys, v)) for v in itertools.product(*values)]
    return experiments


def get_final_data(experiments, d_base):
    result_jsons = []
    for dict_item in experiments:
        tmp_d = str(d_base)
        for key, value in dict_item.items():
            tmp_d = tmp_d.replace(str(key), "'" + str(value) + "'" if isinstance(value, str) else str(value))
        tmp_dict = ast.literal_eval(tmp_d)
        result_jsons.append(tmp_dict)
    return result_jsons


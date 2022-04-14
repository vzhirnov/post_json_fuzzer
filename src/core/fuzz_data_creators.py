import copy
import itertools
import re
import uuid

from src.core.parser.generate import generate_strategy
from src.strategies.methods import make_ast_literal_eval


def get_jsons_for_fuzzing(d_base: dict):
    matched_items, d = get_interesting_data(d_base)
    experiments = get_all_combinations(matched_items)
    jsons = get_final_data(experiments, d)
    return jsons


def get_interesting_data(d_base: dict):
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


def get_all_combinations(matched_items: dict):
    keys, values = zip(*matched_items.items())  # TODO: assert if no ()s with strategy, just plain dict values
    experiments = [dict(zip(keys, v)) for v in itertools.product(*values)]
    return experiments


def find_word_and_add_quotes(str_line: str, interesting_word: str):
    def insert_quote(string, index_num):
        return string[:index_num] + '\'' + string[index_num:]

    start_index = str_line.find(interesting_word)
    end_index = str_line.find(interesting_word) + len(interesting_word)
    res = insert_quote(str_line, start_index)
    res = insert_quote(res, end_index + 1)
    return res


def get_final_data(experiments: list, d_base: str):
    result_jsons = []
    fuzz_item = dict()
    exp_keys = list(experiments[0].keys())

    tmp_d_base = d_base
    for key in exp_keys:
        tmp_d_base = find_word_and_add_quotes(tmp_d_base, key)

    tmp_d_base = eval(tmp_d_base)
    for dict_items in experiments:
        tmp_d = copy.deepcopy(tmp_d_base)
        for key, value in dict_items.items():
            if key in tmp_d:
                tmp_d[value] = tmp_d.pop(key)
                fuzz_item.update({value: tmp_d_base[key]})
            elif list(tmp_d.keys())[list(tmp_d.values()).index(key)]:
                need_key = list(tmp_d.keys())[list(tmp_d.values()).index(key)]
                tmp_d[need_key] = value
                fuzz_item.update({need_key: value})
            else:
                raise Exception("This should never happen")
        res_dict = tmp_d
        result_jsons.append((res_dict, fuzz_item))
        fuzz_item = {}
    return result_jsons


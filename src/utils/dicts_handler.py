import ast

from copy import copy, deepcopy


result = []
path = []


def find_path(dict_obj, key, i=None):
    for k, v in dict_obj.items():
        path.append(k)
        if isinstance(v, dict):
            find_path(v, key, i)
        if isinstance(v, list):
            for i, item in enumerate(v):
                path.append(i)
                if isinstance(item, dict):
                    find_path(item, key, i)
                path.pop()
        if k == key:
            result.append(copy(path))
        if path:
            path.pop()


def find_obj_in_dict_and_replace_it(c_obj, obj_to_replace, replacement_obj):
    if c_obj == obj_to_replace:
        return replacement_obj
    elif isinstance(c_obj, list):
        for i, v in enumerate(c_obj):
            c_obj[i] = find_obj_in_dict_and_replace_it(
                v, obj_to_replace, replacement_obj
            )
    elif isinstance(c_obj, dict):
        for k, v in c_obj.items():
            c_obj[k] = find_obj_in_dict_and_replace_it(
                v, obj_to_replace, replacement_obj
            )
    return c_obj


def get_access_view_to_deep_key(dic_name, path):
    res = str(dic_name)
    for item in path[:-1]:
        if isinstance(item, str):
            item = "'" + item + "'"
        res += "[" + str(item) + "]"
    return res


def deep_sorted(obj, *, key=None, reverse=False):
    if isinstance(obj, dict):
        return {
            k: deep_sorted(v, key=key, reverse=reverse)
            for k, v in sorted(obj.items(), key=key, reverse=reverse)
        }
    if isinstance(obj, list):
        return [
            deep_sorted(v, key=key, reverse=reverse)
            for i, v in sorted(enumerate(obj), key=key, reverse=reverse)
        ]
    return obj


def make_dictionary_items_unique(jsons: list):
    final_jsons = deep_sorted(jsons)
    res_set = set()
    for item in final_jsons:
        res_set.add(str(item))
    res_list = list()
    for item in res_set:
        res_list.append(ast.literal_eval(item))
    return res_list

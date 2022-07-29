import ast
import inspect

from typing import Union, List, Dict, Any

from copy import copy
from src.datastructures.fuzzy import Fuzzy

result = []
path = []


def find_path_for_key(dict_obj: dict, key: Fuzzy, i=None):
    for k, v in dict_obj.items():
        path.append(k)
        if isinstance(v, dict):
            find_path_for_key(v, key, i)
        if isinstance(v, list):
            for i, item in enumerate(v):
                path.append(i)
                if isinstance(item, dict):
                    find_path_for_key(item, key, i)
                path.pop()
        if k == key:
            result.append(copy(path))
        if path:
            path.pop()


def find_path_for_value(dict_obj: Union[Dict, List], value: Fuzzy, i=None):
    if isinstance(dict_obj, list):
        for i, item in enumerate(dict_obj):
            path.append(i)
            if item == value:
                result.append(copy(path))
                return
            if isinstance(item, dict):
                find_path_for_value(item, value, i)
            if isinstance(item, list):
                find_path_for_value(item, value, i)
            path.pop()
    if isinstance(dict_obj, dict):
        for k, v in dict_obj.items():
            path.append(k)
            if isinstance(v, dict):
                find_path_for_value(v, value, i)
            if isinstance(v, list):
                find_path_for_value(v, value, i)
            if v == value:
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


def get_access_view_to_deep_key(dic_name: str, path: list):
    res = str(dic_name)
    for item in path[:-1]:
        if isinstance(item, str):
            item = "'" + item + "'"
        res += "[" + str(item) + "]"
    return res


def get_access_view_to_deep_value(dic_name: str, path: list):
    res = str(dic_name)
    for item in path:
        if isinstance(item, str):
            item = "'" + item + "'"
        res += "[" + str(item) + "]"
    return res


def deep_sorted(lst: Union[Dict, List]):
    def sort_key(e):
        if isinstance(e, list):
            return str([sort_key(inner) for inner in e])
        elif isinstance(e, dict):
            return str(e)
        return str(e)

    if isinstance(lst, list):
        res = [
            deep_sorted(e)
            if isinstance(e, list)
            else {k: v for k, v in sorted(e.items(), key=lambda item: str(item[0]))}
            if isinstance(e, dict)
            else e
            for e in lst
        ]
        return sorted(res, key=sort_key)
    elif isinstance(lst, dict):
        return {
            k: deep_sorted(v)
            for k, v in sorted(lst.items(), key=lambda item: str(item[0]))
        }
    else:
        return lst


def make_dictionary_items_unique(jsons: list):
    final_jsons = deep_sorted(jsons)
    res_set = set()
    for item in final_jsons:
        res_set.add(str(item))
    res_list = list()
    for item in res_set:
        res_list.append(ast.literal_eval(item))
    return res_list


class DLContainer:
    def __init__(self, base_object: dict):
        self.base_object = base_object
        self.base_object_name = self.retrieve_arg_name(base_object).pop()
        self.result = []
        self.path = []

    def retrieve_arg_name(self, var: Any) -> list:
        """
        Get var's name.
        See https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
        :param var: Any object
        :return: var name
        """
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]

    def retrieve_arg_real_name(self, var: Any) -> list:
        """
        Get var's real name.
        See https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
        :param var: Any object
        :return: var name
        """
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
        return [var_name for var_name, var_val in callers_local_vars if var_val is var]

    def clean_data(self):
        self.result.clear()
        self.path.clear()

    def get(self, key_or_value: Any, default_value: None):
        """
        :param key_or_value: key or value to find
        :param default_value: will return if item is not found
        :return: path to item, and digit which is either 0(key is found) or 1(value is found)
        """
        self.clean_data()
        self.find_path_for_key(self.base_object, key_or_value)
        if self.result:
            res = self.result.pop()
            return res, 0
        else:
            self.clean_data()
            self.find_path_for_value(self.base_object, key_or_value)
            if self.result:
                res = self.result.pop()
                return res, 1
        return default_value, None

    def find_path_for_key(self, dict_obj: dict, key: Any, i=None):  # TODO make method private
        for k, v in dict_obj.items():
            self.path.append(k)
            if isinstance(v, dict):
                self.find_path_for_key(v, key, i)
            if isinstance(v, list):
                for i, item in enumerate(v):
                    self.path.append(i)
                    if isinstance(item, dict):
                        self.find_path_for_key(item, key, i)
                    self.path.pop()
            if k == key:
                self.result.append(copy(self.path))
            if self.path:
                self.path.pop()

    def find_path_for_value(self, dict_obj: Union[Dict, List], value: Fuzzy, i=None):  # TODO make method private
        if isinstance(dict_obj, list):
            for i, item in enumerate(dict_obj):
                self.path.append(i)
                if item == value:
                    self.result.append(copy(self.path))
                    return
                if isinstance(item, dict):
                    self.find_path_for_value(item, value, i)
                if isinstance(item, list):
                    self.find_path_for_value(item, value, i)
                self.path.pop()
        if isinstance(dict_obj, dict):
            for k, v in dict_obj.items():
                self.path.append(k)
                if isinstance(v, dict):
                    self.find_path_for_value(v, value, i)
                if isinstance(v, list):
                    self.find_path_for_value(v, value, i)
                if v == value:
                    self.result.append(copy(self.path))
                if self.path:
                    self.path.pop()

    def new_get_access_view_to_deep_key(self, dic_name: str, path: dict):
        d_name = self.retrieve_arg_real_name(path).pop()
        res = str(dic_name)
        max_dict_index = max(list(path.keys()))
        del path[max_dict_index]
        for path_index, path_value in path.items():
            res += "[" + d_name + "[" + str(path_index) + "]" + "]"
        return res

    def new_get_access_view_to_deep_value(self, dic_name: str, path: dict):
        d_name = self.retrieve_arg_real_name(path).pop()
        res = str(dic_name)
        for path_index, path_value in path.items():
            res += "[" + d_name + "[" + str(path_index) + "]" + "]"
        return res

    def set_new_item(self, path: list, new_value: Any):
        pass

    def update_key(self, path: list, new_value: Any):
        base_object = self.base_object  # it is need for exec
        new_path = path
        path_vars = {}
        for i, item in enumerate(new_path):
            path_vars[i] = item

        access_view_to_curr_key = self.new_get_access_view_to_deep_value(
            self.base_object_name, path_vars
        )

        obj_to_replace = new_value if isinstance(new_value, str) else "'" + str(new_value) + "'"

        access_view_to_req_key = self.new_get_access_view_to_deep_key(
            self.base_object_name, path_vars
        ) + str([obj_to_replace])

        for i, item in enumerate(new_path):
            path_vars[i] = item

        add_new_kv = "self." + access_view_to_req_key + " = " + "self." + access_view_to_curr_key
        exec(add_new_kv)

        del_old_kv = "del self." + access_view_to_curr_key
        exec(del_old_kv)
        a = 1

    def update_value(self, path: list, new_value: Any):
        new_path = path
        path_vars = {}
        for i, item in enumerate(new_path):
            path_vars[i] = item

        access_view_to_key = self.new_get_access_view_to_deep_value(
            self.base_object_name, path_vars
        )

        obj_to_replace = new_value if not isinstance(new_value, str) else "'" + str(new_value) + "'"
        base_object = self.base_object
        add_new_kv = "self." + access_view_to_key + " = " + f"{obj_to_replace}"
        exec(add_new_kv)

    def update_item(self, path: list, new_value: Any, key_or_value: int):
        if path is None:
            return
        if key_or_value == 0:
            self.update_key(path, new_value)
        elif key_or_value == 1:
            self.update_value(path, new_value)
        else:
            return

    def delete_item(self, path: list, item_to_delete: Any):
        pass

    def find_obj_in_dict_and_replace_it(self, c_obj, obj_to_replace, replacement_obj):
        if c_obj == obj_to_replace:
            return replacement_obj
        elif isinstance(c_obj, list):
            for i, v in enumerate(c_obj):
                c_obj[i] = self.find_obj_in_dict_and_replace_it(
                    v, obj_to_replace, replacement_obj
                )
        elif isinstance(c_obj, dict):
            for k, v in c_obj.items():
                c_obj[k] = self.find_obj_in_dict_and_replace_it(
                    v, obj_to_replace, replacement_obj
                )
        return c_obj

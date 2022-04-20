from copy import copy, deepcopy

result = []
path = []


# i is the index of the list that dict_obj is part of
def find_path(dict_obj, key, i=None):
    for k, v in dict_obj.items():
        # add key to path
        path.append(k)
        if isinstance(v, dict):
            # continue searching
            find_path(v, key, i)
        if isinstance(v, list):
            # search through list of dictionaries
            for i, item in enumerate(v):
                # add the index of list that item dict is part of, to path
                path.append(i)
                if isinstance(item, dict):
                    # continue searching in item dict
                    find_path(item, key, i)
                # if reached here, the last added index was incorrect, so removed
                path.pop()
        if k == key:
            # add path to our result
            result.append(copy(path))
        # remove the key added in the first line
        if path:
            path.pop()

def get_access_view_to_deep_key(dic_name, path):
    res = str(dic_name)
    for item in path[:-1]:
        if isinstance(item, str):
            item = "'" + item + "'"
        res += '[' + str(item) + ']'
    return res

def set_dict_deep_key_instead_of_current(dic, key_path, current_key, key_to_set):
    d = dic
    for key in key_path:
        if key == current_key:
            d[key_to_set] = d[current_key]
            break
        else:
            d = d[key]
    return d


def set_dict_deep_value_instead_of_current(dic, current_key, key_to_set):
    d = deepcopy(dic)
    return d


def delete_dict_deep_key_value(dic, key_path):
    d = deepcopy(dic)
    return d


def nested_get(dic, keys):
    for key in keys:
        dic = dic[key]
    return dic


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

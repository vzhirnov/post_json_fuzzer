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


def find_obj_in_dict_and_replace_it(c_obj, obj_to_replace, replacement_obj):
    if c_obj == obj_to_replace:
        return replacement_obj
    elif isinstance(c_obj, list):
        for i, v in enumerate(c_obj):
            c_obj[i] = find_obj_in_dict_and_replace_it(v, obj_to_replace, replacement_obj)
    elif isinstance(c_obj, dict):
        for k, v in c_obj.items():
            c_obj[k] = find_obj_in_dict_and_replace_it(v, obj_to_replace, replacement_obj)
    return c_obj


def get_access_view_to_deep_key(dic_name, path):
    res = str(dic_name)
    for item in path[:-1]:
        if isinstance(item, str):
            item = "'" + item + "'"
        res += '[' + str(item) + ']'
    return res

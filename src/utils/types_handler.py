import ast


# TODO there is also restore_data_type, think what to do with names and where to put both of them
def restore_type(lst: list):
    return [ast.literal_eval(x) for x in lst]


def list_once(items):
    if isinstance(items, list):
        return [[i] for i in items]
    return [items]


def list_several_times(items, n):
    if not n.isdigit():
        return items
    else:
        n = ast.literal_eval(n)
    lst = items
    for _ in range(n):
        lst = list_once(lst)
    return lst

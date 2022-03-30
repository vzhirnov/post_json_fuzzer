import ast


def list_current_items(item):
    if isinstance(item, list):
        return [[i] for i in item]
    return [item]


def unlist_current_items(items_list):
    if isinstance(items_list, list) and isinstance(items_list[0], list):
        return items_list.pop()
    return items_list


def restore_data_type(littered_data):
    l = []
    for littered_item in littered_data:
        try:
            c = ast.literal_eval(littered_item)
            l.append(c)
        except Exception as e:
            l.append(littered_item)
    return l


def make_ast_literal_eval(item):
    return [ast.literal_eval(x) for x in item]

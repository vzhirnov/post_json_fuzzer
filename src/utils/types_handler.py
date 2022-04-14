import ast


def restore_type(lst: list):
    return [ast.literal_eval(x) for x in lst]
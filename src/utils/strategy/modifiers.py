import ast
import secrets
import random


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


def restore_data_type(littered_data: list):
    l = []
    type_add_info = ["^s", "^b"]
    for littered_item in littered_data:
        try:
            c = ast.literal_eval(littered_item)
            l.append(c)
        except Exception as e:
            if littered_item.endswith(tuple(type_add_info)):
                index = littered_item.rfind("^")
                littered_item = littered_item[:index]
            l.append(littered_item)
    return l


def make_ast_literal_eval(item):
    return [ast.literal_eval(x) for x in item]


def get_random_unicode(length):
    get_char = chr

    include_ranges = [
        (0x0021, 0x0021),
        (0x0023, 0x0026),
        (0x0028, 0x007E),
        (0x00A1, 0x00AC),
        (0x00AE, 0x00FF),
        (0x0100, 0x017F),
        (0x0180, 0x024F),
        (0x2C60, 0x2C7F),
        (0x16A0, 0x16F0),
        (0x0370, 0x0377),
        (0x037A, 0x037E),
        (0x0384, 0x038A),
        (0x038C, 0x038C),
    ]

    alphabet = [
        get_char(code_point) for current_range in include_ranges
        for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return ''.join(random.choice(alphabet) for i in range(length))


def mutate_any_type(item):
    if isinstance(item, str):
        if not item:
            return get_random_unicode(100)
        rand_index = random.randrange(0, len(item)) if len(item) > 2 else 0
        var1 = item[:rand_index] + "\x00" + str(secrets.token_hex(5)) + "\x00" + str(item[rand_index:])
        var2 = get_random_unicode(random.randrange(100))
        return random.choice([var1, var2])
    elif isinstance(item, int):
        return random.randrange(-10000000, 10000000)
    elif isinstance(item, float):
        return random.uniform(-10000000, 10000000)
    elif isinstance(item, bool):
        return not item
    elif isinstance(item, dict):
        return dict({mutate_any_type(key): mutate_any_type(value) for key, value in item.items()})
    return 0


def mutate(item):
    if isinstance(item, list):
        return item + [mutate_any_type(x) for x in item]
    return mutate_any_type(item)

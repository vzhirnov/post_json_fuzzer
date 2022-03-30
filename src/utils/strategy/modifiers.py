import ast
import secrets
import random
import string
import copy


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
        rand_index = random.randrange(len(item)) if len(item) else 0
        var1 = item[:rand_index] + "\x00" + str(secrets.token_hex(5)) + "\x00" + str(item[rand_index:])
        var2 = get_random_unicode(random.randrange(len(item)))
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

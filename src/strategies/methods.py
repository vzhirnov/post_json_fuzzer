import random
import pyradamsa
import base64

from collections.abc import Iterable


def mutate_by_radamsa(item):
    rad = pyradamsa.Radamsa()
    fuzzed_item = rad.fuzz(bytes(str(item), "utf-8"), seed=random.randrange(10000))
    try:
        decoded_item = fuzzed_item.decode()
        # eval(decoded_item)  need to?
        return decoded_item
    except Exception:
        return fuzzed_item


def mutate_all_by_radamsa(items):
    res = []
    if isinstance(items, Iterable):
        items_types = [type(x) for x in items]
        mutated_items = [mutate_by_radamsa(x) for x in items]
        for i, item in enumerate(mutated_items):
            try:
                elem = (
                    items_types[i](item)
                    if type(item) == items_types[i]
                    else base64.b64encode(item).decode("ascii")
                )
                res.append(elem)
            except Exception:
                res.append(item)
        return res
    return mutate_by_radamsa(items)


def add_border_cases(left_num: int, right_num: int):
    if not isinstance(left_num, int) or not isinstance(right_num, int):
        return [0]
    return list((left_num - 1, left_num, right_num, right_num + 1))

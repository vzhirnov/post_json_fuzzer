import ast
import re
import itertools


# TODO: add null in stratgies
# TODO: make interactive work with 500 responses:
#  repeat 500th requests until all random 500th answers turn into 200th answers
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def pop_all(self):
        r, self.items[:] = self.items[:], []
        return r

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


STRATEGY_1 = [0, 1, 2, 3, 4]
STRATEGY_2 = [5, 6, 7, 8, 9]
STAR = [11, 22, 33, 44, 55]

def parser_view(text):
    # TODO: are \[| with \]| really need?
    numbers = r"""(?x)(
    \d+|
    \w+|
    \*|
    \+|
    \^|
    \{.*?\}| 
    \[.*?\]| 
    \[\[\]]|
    \[|
    \]|
    \b
    )
    """
    a = re.findall(numbers, text)
    res = [x for x in a if x != '']
    return res


def list_current_items(items_list):
    return [[i] for i in items_list]


def unlist_current_items(items_list):
    if isinstance(items_list, list) and isinstance(items_list[0], list):
        return items_list.pop()
    return items_list


def generate_strategy(strategy_info):
    # TODO: migrate assert upper where it is really required
    assert isinstance(strategy_info, str)  # and all(x not in strategy_info for x in ['(', ')'])
    # TODO: add asserts:
    # TODO: num of opened [s is equal to ]s
    strategy = parser_view(strategy_info)
    stack = Stack()
    result_strategy = []
    for item in strategy:
        if item == 'STRATEGY_1':
            elem = stack.pop()
            result_strategy.insert(0, elem)
            result_strategy += STRATEGY_1
            stack.push(result_strategy)
            result_strategy = []
        elif item == 'STRATEGY_2':
            elem = stack.pop()
            result_strategy.insert(0, elem)
            result_strategy += STRATEGY_2
            stack.push(result_strategy)
            result_strategy = []
        elif item == 'STAR':
            elem = stack.pop()
            result_strategy.insert(0, elem)
            result_strategy += STAR
            stack.push(result_strategy)
            result_strategy = []
        elif item == '^':
            elem = stack.pop()
            if elem == '[]':
                result_strategy = stack.pop()
                result_strategy = list_current_items(result_strategy)
                stack.push(result_strategy)
                result_strategy = []
        elif item == '+':
            elem1 = stack.pop()
            elem2 = stack.pop()
            result_strategy = elem1 + elem2
            stack.push(result_strategy)
            result_strategy = []
        else:
            stack.push(item)
    return unlist_current_items(stack.pop_all())


d_base = {
    # "clientid": (132, 'STRATEGY_1'),
    # "type": ("disable_attack_type", 'STRATEGY_2'),
    # "attack_type": (["xss"], 'STAR'),
    # "point": ("action_ext_1", 'STRATEGY_1', "[]^[]^", "action_ext_2", 'STRATEGY_2', "[]^", "action_ext_star", 'STAR', '++'),
    # "dict_field": ({"point": ["path", 0], "type": "absent"}, 'STAR'),
    # "validated": (True, False),

    # ("action", "another_action",):
    #     [
    #         {("point", '*'): ["header", "HOST"], "type": ("iequal", "equal", "absent"), "value": ("test.com", '*')},
    #         {"point": ["path", 0], "type": "absent"},
    #         {"point": ["action_name"], "type": "equal", "value": ""},
    #         {"point": ["action_ext"], "type": "absent"}
    #     ],
    "token": "1b64c60e7d3e5cdabd63ba61f6e997ee",
}

d = str(d_base)

res = re.findall(r'\(.*?\)', d)

matched_items = dict()

for index, item in enumerate(res):
    matched_index = f"'in_processing_{str(index)}'"
    d = d.replace(item, matched_index)
    matched_index = matched_index.replace('\'', '')
    matched_items[matched_index] = item  # .strip("()")

for key, value in matched_items.items():
    matched_items[key] = generate_strategy(value)

print("base d:\n" + d)
print("matched_items:\n", matched_items)

# ====================
keys, values = zip(*matched_items.items())  # TODO: assert if no ()s with strategy, just plain dict values
experiments = [dict(zip(keys, v)) for v in itertools.product(*values)]
print(len(experiments))
# print(experiments)
# ====================

d = ast.literal_eval(d)
print("d after ast:\n", d)

result_jsons = []
for dict_item in experiments:
    tmp_dict = dict()
    for key, value in d.items():
        if value not in dict_item.keys():
            tmp_dict[key] = value
        else:
            tmp_dict[key] = dict_item[value]
    result_jsons.append(tmp_dict)

print("result_jsons:\n", result_jsons)

from src.strategies.datasets import default
from src.strategies.generators import int_nums_in_range
from src.strategies.methods import (
    mutate_all_by_radamsa,
    mutate_by_radamsa,
    add_border_cases,
    add_from_file,
    get_pack_by_methods,
    list_once,
    list_several_times,
)

data_sets = {"default": default}

methods = {
    "add_border_cases": add_border_cases,
    "mutate_all_elements_by_radamsa": mutate_all_by_radamsa,
    "mutate_by_radamsa": mutate_by_radamsa,
    "add_from_file": add_from_file,
    "get_pack_by_methods": get_pack_by_methods,
    "list_once": list_once,
    "list_several_times": list_several_times,
}

generators = {"int_nums_in_range": int_nums_in_range}

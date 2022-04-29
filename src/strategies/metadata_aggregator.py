from src.strategies.data_sets import default
from src.strategies.generators import int_nums_in_range
from src.strategies.methods import (
    mutate_all_by_radamsa,
    mutate_by_radamsa,
    add_border_cases,
)


data_sets = {"default": default}

methods = {
    "add_border_cases": add_border_cases,
    "mutate_all_elements_by_radamsa": mutate_all_by_radamsa,
    "mutate_by_radamsa": mutate_by_radamsa,
}

generators = {"int_nums_in_range": int_nums_in_range}

from src.utils.handlers.dicts import *


def smart_replace(base_str: str, substr_to_replace: str, on_what_to_replace):
    if substr_to_replace not in base_str:
        return base_str
    if isinstance(on_what_to_replace, str):
        return base_str.replace(substr_to_replace, on_what_to_replace, 1)
    else:
        found_substr_start_index = base_str.find(substr_to_replace)
        found_substr_end_index = base_str.find(substr_to_replace) + len(
            substr_to_replace
        )
        a = base_str[found_substr_start_index - 1]
        b = base_str[found_substr_end_index]
        quotes = "\"'"
        if any(elem in a for elem in quotes) or any(elem in b for elem in quotes):
            replace_item = str(on_what_to_replace)
            base_str = base_str.replace(substr_to_replace, replace_item)
            base_str = (
                base_str[: found_substr_start_index - 1]
                + base_str[found_substr_start_index:]
            )
            replace_item_curr_start_index = found_substr_start_index - 1
            base_str = (
                base_str[: replace_item_curr_start_index + len(replace_item)]
                + base_str[replace_item_curr_start_index + len(replace_item) + 1 :]
            )
    return base_str


def smart_remove(base_str: str, substr_to_remove: str):
    base_dict = eval(base_str)
    if base_dict.get(substr_to_remove, None):
        del base_dict[substr_to_remove]
    else:
        find_path_for_value(base_dict, substr_to_remove)
        if len(result) > 0:
            path_to_curr_deep_value = result.pop()
            access_view_to_value = get_access_view_to_deep_value(
                "base_dict", path_to_curr_deep_value
            )
            a = "del " + access_view_to_value
            exec(a)
        else:
            find_path_for_key(base_dict, substr_to_remove)
            path_to_curr_deep_key = result.pop()

            access_view_to_key = get_access_view_to_deep_key(
                "base_dict", path_to_curr_deep_key
            )
            a = "del " + access_view_to_key + f"['{substr_to_remove}']"
            exec(a)
    result.clear()
    path.clear()
    return str(base_dict)

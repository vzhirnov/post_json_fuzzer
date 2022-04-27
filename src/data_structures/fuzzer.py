from typing import Tuple
# import uuid

# from copy import deepcopy
from collections import defaultdict

from src.data_structures.fuzzy import Fuzzy
from src.utils.strings_handler import smart_replace
from src.utils.dicts_handler import *
from src.core.combinator import Combinator
from src.utils.types_handler import is_evaluable  # make_evaluable

class Fuzzer:

    def __init__(self, json_with_fuzzies: dict):
        self.json_with_fuzzies = deepcopy(json_with_fuzzies)
        self.json_with_uuids, self.fuzzies = self.indexate_fuzzies(json_with_fuzzies)
        self.default_json_body = self.get_default_json_body(self.json_with_uuids)
        self.result_jsons_for_fuzzing = []
        self.default_suspicious_responses = [500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511]

    def get_default_json_body(self, json_with_uuids: dict) -> dict:
        json_with_uuids = str(json_with_uuids)
        for k, v in self.fuzzies.items():
            json_with_uuids = smart_replace(json_with_uuids, k, v.default_value)
        return eval(json_with_uuids)

    def make_final_jsons(self, json_with_uuids: dict, values: list) -> list:
        final_jsons = []
        for pairs in values:
            fuzzies_keys = list(self.fuzzies.keys())
            json_subject = str(deepcopy(json_with_uuids))
            suspicious_replies = []
            for pair in pairs:
                if pair[2]:
                    suspicious_replies += pair[2]
                fuzzies_keys.remove(pair[0])
                json_subject = smart_replace(json_subject, pair[0], pair[1])
            for fuzzy_item_by_default in fuzzies_keys:
                json_subject = smart_replace(json_subject, fuzzy_item_by_default, self.fuzzies[fuzzy_item_by_default].default_value)
            if is_evaluable(json_subject):
                json_subject = eval(json_subject)
                final_jsons.append((json_subject, suspicious_replies))
        return final_jsons

    def get_result_jsons_for_fuzzing(self):
        scenario = {}

        for fuzzy_k, fuzzy_v in self.fuzzies.items():
            suspicious_reply = self.fuzzies[fuzzy_k].suspicious_responses
            scenario[fuzzy_v.test_method] = [[(fuzzy_k, x, suspicious_reply) for x in fuzzy_v.tape]] if scenario.get(fuzzy_v.test_method) is None \
                else scenario[fuzzy_v.test_method] + [[(fuzzy_k, x, suspicious_reply) for x in fuzzy_v.tape]]

        combinator = Combinator()
        for test_method, values in scenario.items():
            scenario[test_method] = combinator.make_variants(*scenario[test_method], test_method=test_method)

        for test_method, values in scenario.items():
            scenario[test_method] = self.make_final_jsons(self.json_with_uuids, values)

        for item in scenario.values():
            self.result_jsons_for_fuzzing += item

        return self.result_jsons_for_fuzzing

    def indexate_fuzzies(self, json_like_obj: dict) -> Tuple[dict, dict]:
        """
        returns res dict with uuids instead of Fs, dict like {uuid1: F1, uuid2: F2} etc
        """
        d_res = deepcopy(json_like_obj)
        stack = list(d_res.items())
        visited = set()
        fuzzies = dict()
        unique_counter = 0
        while stack:
            unique_counter += 1
            k, v = stack.pop()
            if isinstance(k, Fuzzy):
                uuid_key = k.obj_id
                fuzzies[uuid_key] = k

                if k in d_res:
                    d_res[uuid_key] = d_res[k]
                    del d_res[k]
                else:
                    find_path(d_res, k)
                    path_to_curr_deep_key = result.pop()
                    path_to_required_old_deep_key = path_to_curr_deep_key[:-1] + [uuid_key]

                    access_view_to_key = get_access_view_to_deep_key('d_res', path_to_curr_deep_key)
                    a = access_view_to_key + f"['{uuid_key}']" + " = " + f"{v}"
                    exec(a)

                    access_view_to_old_deep_key = get_access_view_to_deep_key('d_res', path_to_required_old_deep_key)

                    b = "del " + access_view_to_old_deep_key + f"[k]"
                    exec(b)

            if isinstance(v, Fuzzy):
                uuid_key = v.obj_id
                fuzzies[uuid_key] = v

                if k in fuzzies.values():
                    for key, value in fuzzies.items():
                        if value == k:
                            need_key = key
                            d_res[need_key] = uuid_key
                            break
                else:
                    d_res = find_obj_in_dict_and_replace_it(d_res, v, uuid_key)

            # make all k:v items unique, even if they are identical
            # but are in different places in the dictionary
            kv_ids_sum = id(k) + id(v) % unique_counter  # TODO: delete it due to smart obj_id hashing

            if isinstance(v, dict):
                if kv_ids_sum not in visited:
                    stack.extend(v.items())
                    continue
            if isinstance(v, list):
                if kv_ids_sum not in visited:
                    if any(isinstance(x, Fuzzy) for x in v):
                        for i, item in enumerate(v):
                            if isinstance(item, Fuzzy):
                                uuid_key = item.obj_id
                                fuzzies[uuid_key] = item
                                v[i] = uuid_key
                    else:
                        stack.extend(({i: x for i, x in enumerate(v)}).items())
                        continue
            visited.add(kv_ids_sum)
        return d_res, fuzzies

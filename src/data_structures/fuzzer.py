from typing import Tuple, List
from copy import deepcopy

from src.data_structures.fuzzy import Fuzzy
from src.utils.strings_handler import smart_replace, smart_remove
from src.utils.dicts_handler import *
from src.core.combinator import Combinator
from src.utils.types_handler import is_evaluable
from src.data_structures.metadata import Metadata


class Fuzzer:
    def __init__(self, json_with_fuzzies: dict):
        self.json_with_fuzzies = deepcopy(json_with_fuzzies)
        self.json_with_uuids, self.fuzzies = self.indexate_fuzzies(json_with_fuzzies)
        self.default_json_body = self.get_default_json_body(self.json_with_uuids)
        self.result_jsons_for_fuzzing = []
        self.default_suspicious_responses = [
            500,
            501,
            502,
            503,
            504,
            505,
            506,
            507,
            508,
            510,
            511,
        ]

    def get_default_json_body(self, json_with_uuids: dict) -> dict:
        json_with_uuids = str(json_with_uuids)
        for k, v in self.fuzzies.items():
            json_with_uuids = smart_replace(json_with_uuids, k, v.default_value)
        return eval(json_with_uuids)

    def make_final_jsons(self, json_with_uuids: dict, bundle: list) -> list:
        final_jsons = []
        for metadata_package in bundle:
            suspicious_replies = []
            if isinstance(metadata_package, List) and all(
                isinstance(x, Metadata) for x in metadata_package
            ):
                for metadata in metadata_package:
                    json_subject = str(deepcopy(json_with_uuids))
                    fuzzies_keys = list(self.fuzzies.keys())
                    if metadata.suspicious_reply:
                        suspicious_replies += metadata.suspicious_reply
                    fuzzies_keys.remove(
                        metadata.uuid
                    ) if metadata.uuid in fuzzies_keys else True

                    if metadata.enabled is False:
                        json_subject = smart_remove(
                            json_subject, metadata.uuid
                        )
                    else:
                        json_subject = smart_replace(
                            json_subject, metadata.uuid, metadata.fuzz_data
                        )

                    for fuzzy_item_by_default in fuzzies_keys:
                        json_subject = smart_replace(
                            json_subject,
                            fuzzy_item_by_default,
                            self.fuzzies[fuzzy_item_by_default].default_value,
                        )
                    if is_evaluable(json_subject):
                        json_subject = eval(json_subject)
                        final_jsons.append(
                            (json_subject, list(set(suspicious_replies)))
                        )
            else:
                for metadata_item in metadata_package:
                    json_subject = str(deepcopy(json_with_uuids))
                    fuzzies_keys = list(self.fuzzies.keys())
                    for metadata in metadata_item:
                        if metadata.suspicious_reply:
                            suspicious_replies += metadata.suspicious_reply
                        fuzzies_keys.remove(
                            metadata.uuid
                        ) if metadata.uuid in fuzzies_keys else True
                        json_subject = smart_replace(
                            json_subject, metadata.uuid, metadata.fuzz_data
                        )

                    for fuzzy_item_by_default in fuzzies_keys:
                        json_subject = smart_replace(
                            json_subject,
                            fuzzy_item_by_default,
                            self.fuzzies[fuzzy_item_by_default].default_value,
                        )
                    if is_evaluable(json_subject):
                        json_subject = eval(json_subject)
                        final_jsons.append(
                            (json_subject, list(set(suspicious_replies)))
                        )

        final_jsons = make_dictionary_items_unique(final_jsons)
        return final_jsons

    def get_result_jsons_for_fuzzing(self) -> list:
        scenario = {}
        for fuzzy_uuid, fuzzy_itself in self.fuzzies.items():
            suspicious_reply = fuzzy_itself.suspicious_responses
            scenario[fuzzy_itself.test_method] = (
                [
                    [
                        Metadata(fuzzy_uuid, data_set_item, suspicious_reply)
                        for data_set_item in fuzzy_itself.tape
                    ]
                ]
                if scenario.get(fuzzy_itself.test_method) is None
                else scenario[fuzzy_itself.test_method]
                + [
                    [
                        Metadata(fuzzy_uuid, data_set_item, suspicious_reply)
                        for data_set_item in fuzzy_itself.tape
                    ]
                ]
            )

        combinator = Combinator(scenario, self.default_json_body)
        for test_method, _ in scenario.items():
            scenario[test_method] = combinator.make_variants(test_method=test_method)

        for test_method, metadata_bundle in scenario.items():
            scenario[test_method] = self.make_final_jsons(
                self.json_with_uuids, metadata_bundle
            )

        for item in scenario.values():
            self.result_jsons_for_fuzzing += item
        return self.result_jsons_for_fuzzing

    def indexate_fuzzies(self, json_like_obj: dict) -> Tuple[dict, dict]:
        """
        returns res dict with uuids instead of Fs, dict like {uuid1: F1, uuid2: F2, uuid3: uuid4}
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
                if k.enabled is False:
                    find_path_for_key(d_res, k)
                    path_to_curr_deep_key = result.pop()
                    path_to_required_old_deep_key = path_to_curr_deep_key[:-1] + [
                        uuid_key
                    ]

                    access_view_to_key = get_access_view_to_deep_key(
                        "d_res", path_to_curr_deep_key
                    )
                    a = access_view_to_key + f"['{k.default_value}']" + " = " + "v"
                    exec(a)

                    access_view_to_old_deep_key = get_access_view_to_deep_key(
                        "d_res", path_to_required_old_deep_key
                    )

                    b = "del " + access_view_to_old_deep_key + f"[k]"
                    exec(b)
                else:

                    uuid_key = k.obj_id
                    fuzzies[uuid_key] = k

                    if k in d_res:
                        d_res[uuid_key] = d_res[k]
                        del d_res[k]
                    else:
                        find_path_for_key(d_res, k)
                        path_to_curr_deep_key = result.pop()
                        path_to_required_old_deep_key = path_to_curr_deep_key[:-1] + [
                            uuid_key
                        ]

                        access_view_to_key = get_access_view_to_deep_key(
                            "d_res", path_to_curr_deep_key
                        )
                        a = access_view_to_key + f"['{uuid_key}']" + " = " + "v"
                        exec(a)

                        access_view_to_old_deep_key = get_access_view_to_deep_key(
                            "d_res", path_to_required_old_deep_key
                        )

                        b = "del " + access_view_to_old_deep_key + f"[k]"
                        exec(b)

            if isinstance(v, Fuzzy):
                uuid_key = v.obj_id
                if v.enabled is False:
                    find_path_for_value(d_res, v)
                    path_to_curr_deep_value = result.pop()
                    access_view_to_value = get_access_view_to_deep_value(
                        "d_res", path_to_curr_deep_value
                    )
                    a = access_view_to_value + " = " + \
                        (f"{v.default_value}" if not isinstance(v.default_value, str) else f"'{v.default_value}'")
                    exec(a)
                    continue
                fuzzies[uuid_key] = v

                if k in d_res.values():
                    if k in fuzzies.values():
                        for key, value in fuzzies.items():
                            if value == k:
                                need_key = key
                                d_res[need_key] = uuid_key
                                break
                    else:
                        d_res = find_obj_in_dict_and_replace_it(d_res, v, uuid_key)
                else:
                    find_path_for_value(d_res, v)
                    path_to_curr_deep_value = result.pop()
                    access_view_to_value = get_access_view_to_deep_value(
                        "d_res", path_to_curr_deep_value
                    )
                    a = access_view_to_value + " = " + f"'{uuid_key}'"
                    exec(a)

            # make all k:v items unique, even if they are identical
            # but are in different places in the dictionary
            kv_ids_sum = (
                id(k) + id(v) % unique_counter
            )  # TODO: check if this could be removed because of smart obj_id hashing

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

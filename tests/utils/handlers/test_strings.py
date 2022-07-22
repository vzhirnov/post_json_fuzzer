import pytest

from src.utils.handlers.strings import smart_replace, smart_remove


class TestStrings:

    @pytest.mark.parametrize(
        "base_str, str_to_remove, expected_result",
        [
            ("{'str': 1, '2': 2, '3': 3}", 'str', "{'2': 2, '3': 3}"),
            ("{'1': 'str', '2': 2, '3': 3}", 'str', "{'2': 2, '3': 3}"),

            ("{'str': 1}", 'str', "{}"),
            ("{'1': 'str'}", 'str', "{}"),

            # ("{'1': {'str': 4}, '2': 2, '3': 3}", 'str', "{'1': {}, '2': 2, '3': 3}"),  TODO bug
            ("{'1': {4: 'str'}, '2': 2, '3': 3}", 'str', "{'1': {}, '2': 2, '3': 3}"),

            # ("{'1': ['str', 'other_str']}", 'str', "{'1': ['other_str']}"),  # TODO bug
            # ("{'1': ['str']}", 'str', "{}"),  # TODO bug

            # ("{'1': 1, '2': 2, '3': [{'str': 4, '5':5}, {'6':6}]}", 'str', "{'1': 1, '2': 2, '3': [{'5':5}, {'6':6}]}"),  TODO bug
            ("{'1': 1, '2': 2, '3': [{'4': 'str', '5':5}, {'6':6}]}", 'str',
             "{'1': 1, '2': 2, '3': [{'5':5}, {'6':6}]}"),

            # ("{'1': 1, '2': 2, '3': {'4': ['str'], '5':5}}", 'str', "{'1': 1, '2': 2, '3': {'5':5}}"),  TODO bug
        ],
    )
    def test_smart_remove(self, base_str, str_to_remove, expected_result):
        assert eval(smart_remove(base_str, str_to_remove)) == eval(expected_result)

    @pytest.mark.parametrize(
        "base_str, str_to_replace, str_on_what_to_replace, expected_result",
        [
            ("{'str': 1, '2': 2, '3': 3}", 'str', 'str1', "{'str1': 1, '2': 2, '3': 3}"),
            ("{'1': 'str', '2': 2, '3': 3}", 'str', 'str1', "{'1': 'str1', '2': 2, '3': 3}"),

            ("{'1': {'str': 4}, '2': 2, '3': 3}", 'str', 'str1', "{'1': {'str1': 4}, '2': 2, '3': 3}"),
            ("{'1': {4: 'str'}, '2': 2, '3': 3}", 'str', 'str1', "{'1': {4: 'str1'}, '2': 2, '3': 3}"),

            # ("{'1': ['str', 'other_str']}", 'str', 'str1', "{'1': ['str1', 'other_str']}"), TODO bug
            ("{'1': ['str']}", 'str', 'str1', "{'1': ['str1']}"),

            (
                    "{'1': 1, '2': 2, '3': [{'str': 4, '5':5}, {'6':6}]}",
                    'str', 'str1',
                    "{'1': 1, '2': 2, '3': [{'str1': 4, '5':5}, {'6':6}]}"
            ),
            (
                    "{'1': 1, '2': 2, '3': [{'4': 'str', '5':5}, {'6':6}]}",
                    'str', 'str1',
                    "{'1': 1, '2': 2, '3': [{'4': 'str1', '5':5}, {'6':6}]}"
            ),

            (
                    "{'1': 1, '2': 2, '3': {'4': ['str'], '5':5}}",
                    'str', 'str1',
                    "{'1': 1, '2': 2, '3': {'4': ['str1'], '5':5}}"
            ),
        ],
    )
    def test_smart_replace(self, base_str, str_to_replace, str_on_what_to_replace, expected_result):
        assert eval(smart_replace(base_str, str_to_replace, str_on_what_to_replace)) == eval(expected_result)

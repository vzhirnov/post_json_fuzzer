import pytest

from src.data_structures.fuzzer import Fuzzer, Fuzzy


@pytest.mark.parametrize(
    "json_with_fuzzies, required_fuzzies_num, expected_default_json_body",
    [
        ({
             "point": Fuzzy("my_point", ("1",))
         }, 1, {
             'point': 'my_point'
         }), ({
                  Fuzzy("my_point", ("1",)): "point"
              }, 1, {
                  'my_point': 'point'
              }),
        (
                {
                    Fuzzy(default_value="clientid", scenario=(1, "test")): Fuzzy(default_value=132, scenario=(133,))
                },
                2, {
                    'clientid': 132
                }
        ),
        (
                {
                    "action": [{
                        "point1": Fuzzy(default_value="within_action", scenario=("1",))
                    }, ],
                },
                1, {
                    'action': [{
                        'point1': 'within_action'
                    }]
                }
        ),
        (
                {
                    "action": [{
                        Fuzzy(default_value=None, scenario=(133,)): ["action_ext"], "type": "absent"
                    }]
                },
                1, {
                    'action': [{
                        None: ['action_ext'], 'type': 'absent'
                    }]
                }
        ),
        (
                {
                    Fuzzy(default_value="clientid", scenario=(1, "test")): Fuzzy(default_value=132, scenario=(133,)),
                    "point": Fuzzy("my_point", ("1",)),
                    "action": [
                        {
                            "point1": Fuzzy(default_value="within_action", scenario=("1",))
                        }, {
                            Fuzzy(default_value=None, scenario=(133,)): ["action_ext"], "type": "absent"
                        }
                    ],
                    Fuzzy(default_value="some_test_key", scenario=(12, "some_test")): 1
                },
                6,
                {
                    'action': [{
                        'point1': 'within_action'
                    }, {
                        None: ['action_ext'], 'type': 'absent'
                    }],
                    'clientid': 132,
                    'point': 'my_point',
                    'some_test_key': 1
                }
        ),
        (
                {
                    "action": [Fuzzy(default_value="within_action", scenario=("1",))]
                },
                1,
                {'action': ['within_action']}
        ),
        (
                {
                    "action": [
                        Fuzzy(default_value="within_action_0", scenario=("1",)),
                        Fuzzy(default_value="within_action_1", scenario=("1",))
                    ]
                },
                2,
                {'action': ['within_action_0', 'within_action_1']}
        )
    ]
)
def test_indexate_fuzzies(json_with_fuzzies: dict, required_fuzzies_num: int, expected_default_json_body: dict) -> None:
    fuzzer = Fuzzer(json_with_fuzzies)
    assert len(fuzzer.fuzzies) == required_fuzzies_num
    assert fuzzer.default_json_body == expected_default_json_body

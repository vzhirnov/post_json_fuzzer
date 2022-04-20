import pytest

from src.core.fuzz_data_creators import get_jsons_for_fuzzing


@pytest.mark.parametrize(
    "json_with_dsl, expected_jsons",
    [
        ({
            "clientid": (132, 133)
        }, [({
            'clientid': 132
        }, {
            'clientid': 132
        }), ({
            'clientid': 133
        }, {
            'clientid': 133
        })]),
        (
            {
                "clientid": (132, 133), "test": 1
            }, [({
                'clientid': 132, 'test': 1
            }, {
                'clientid': 132
            }), ({
                'clientid': 133, 'test': 1
            }, {
                'clientid': 133
            })]
        ),
        (
            {
                ("clientid", "other_client_id"): (132, 133)
            },
            [
                ({
                    'clientid': 132
                }, {
                    'clientid': 132
                }), ({
                    'clientid': 133
                }, {
                    'clientid': 133
                }), ({
                    'other_client_id': 132
                }, {
                    'other_client_id': 132
                }), ({
                    'other_client_id': 133
                }, {
                    'other_client_id': 133
                })
            ]
        ),
        (
            {
                "action": [{
                    "point": ["header", ("HOST", "NO_HOST")], "type": "iequal", "value": "test.com"
                }]
            },
            [
                (
                    {
                        'action': [{
                            'point': ['header', 'HOST'], 'type': 'iequal', 'value': 'test.com'
                        }]
                    }, {
                        'HOST': "['header', 'HOST']"
                    }
                ),
                (
                    {
                        'action': [{
                            'point': ['header', 'NO_HOST'], 'type': 'iequal', 'value': 'test.com'
                        }]
                    }, {
                        'NO_HOST': "['header', 'NO_HOST']"
                    }
                )
            ]
        ),
    ]
)
def test_jsons_for_fuzzing(json_with_dsl: dict, expected_jsons: list) -> None:
    assert get_jsons_for_fuzzing(json_with_dsl) == expected_jsons

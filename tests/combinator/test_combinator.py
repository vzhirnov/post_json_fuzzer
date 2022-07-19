import pytest

from src.core.combinator import Combinator
from src.data_structures.test_method import TestMethod
from src.data_structures.metadata import Metadata


class TestCombinator:
    @pytest.mark.parametrize(
        "metadata_bundle, expected_result",
        [
            (
                [
                    [Metadata("c972b612-df65-4d99-923b-8494d88b0ac5", 1, [200])],
                    [Metadata("c972b612-df65-4d99-923b-8494d88b0ac6", 2, [200])],
                ],
                [
                    Metadata("c972b612-df65-4d99-923b-8494d88b0ac5", 1, [200]),
                    Metadata("c972b612-df65-4d99-923b-8494d88b0ac6", 2, [200]),
                ],
            ),
        ],
    )
    def test_take_curr_and_others_by_def(self, scenario: list, expected_result):
        c = Combinator()
        assert c.take_curr_and_others_by_def(scenario) == expected_result

    @pytest.mark.parametrize(
        "metadata_bundle, expected_result",
        [
            (
                [
                    [
                        [Metadata("1972b612-df65-4d99-923b-8494d88b0ac1", 1, [200])],
                        [Metadata("2972b612-df65-4d99-923b-8494d88b0ac2", 2, [200])],
                        [Metadata("3972b612-df65-4d99-923b-8494d88b0ac3", 3, [200])],
                    ],
                    [
                        [Metadata("4972b612-df65-4d99-923b-8494d88b0ac4", 4, [200])],
                        [Metadata("5972b612-df65-4d99-923b-8494d88b0ac5", 5, [200])],
                    ],
                ],
                [
                    [
                        [Metadata("1972b612-df65-4d99-923b-8494d88b0ac1", 1, [200])],
                        [Metadata("4972b612-df65-4d99-923b-8494d88b0ac4", 4, [200])],
                    ],
                    [
                        [Metadata("2972b612-df65-4d99-923b-8494d88b0ac2", 2, [200])],
                        [Metadata("4972b612-df65-4d99-923b-8494d88b0ac4", 4, [200])],
                    ],
                    [
                        [Metadata("3972b612-df65-4d99-923b-8494d88b0ac3", 3, [200])],
                        [Metadata("4972b612-df65-4d99-923b-8494d88b0ac4", 4, [200])],
                    ],
                    [
                        [Metadata("3972b612-df65-4d99-923b-8494d88b0ac3", 3, [200])],
                        [Metadata("5972b612-df65-4d99-923b-8494d88b0ac5", 5, [200])],
                    ],
                    [
                        [Metadata("2972b612-df65-4d99-923b-8494d88b0ac2", 2, [200])],
                        [Metadata("5972b612-df65-4d99-923b-8494d88b0ac5", 5, [200])],
                    ],
                    [
                        [Metadata("1972b612-df65-4d99-923b-8494d88b0ac1", 1, [200])],
                        [Metadata("5972b612-df65-4d99-923b-8494d88b0ac5", 5, [200])],
                    ],
                ],
            ),
        ],
    )
    def test_make_pair_wise(self, scenario: list, expected_result):
        c = Combinator()
        assert c.make_pair_wise(scenario) == expected_result

    @pytest.mark.parametrize(
        "metadata_bundle, expected_result",
        [
            (
                [
                    [
                        [Metadata("1972b612-df65-4d99-923b-8494d88b0ac5", 1, [200])],
                        [Metadata("2972b612-df65-4d99-923b-8494d88b0ac6", 2, [200])],
                    ],
                    [
                        Metadata("3972b612-df65-4d99-923b-8494d88b0ac5", 3, [200]),
                        Metadata("4972b612-df65-4d99-923b-8494d88b0ac4", 4, [200]),
                        Metadata("5972b612-df65-4d99-923b-8494d88b0ac5", 5, [200]),
                    ],
                ],
                [
                    (
                        [Metadata("1972b612-df65-4d99-923b-8494d88b0ac5", 1, [200])],
                        Metadata("3972b612-df65-4d99-923b-8494d88b0ac5", 3, [200]),
                    ),
                    (
                        [Metadata("1972b612-df65-4d99-923b-8494d88b0ac5", 1, [200])],
                        Metadata("4972b612-df65-4d99-923b-8494d88b0ac4", 4, [200]),
                    ),
                    (
                        [Metadata("1972b612-df65-4d99-923b-8494d88b0ac5", 1, [200])],
                        Metadata("5972b612-df65-4d99-923b-8494d88b0ac5", 5, [200]),
                    ),
                    (
                        [Metadata("2972b612-df65-4d99-923b-8494d88b0ac6", 2, [200])],
                        Metadata("3972b612-df65-4d99-923b-8494d88b0ac5", 3, [200]),
                    ),
                    (
                        [Metadata("2972b612-df65-4d99-923b-8494d88b0ac6", 2, [200])],
                        Metadata("4972b612-df65-4d99-923b-8494d88b0ac4", 4, [200]),
                    ),
                    (
                        [Metadata("2972b612-df65-4d99-923b-8494d88b0ac6", 2, [200])],
                        Metadata("5972b612-df65-4d99-923b-8494d88b0ac5", 5, [200]),
                    ),
                ],
            ),
        ],
    )
    def test_make_all_combinations(self, scenario: list, expected_result):
        c = Combinator()
        assert c.make_all_combinations(scenario) == expected_result

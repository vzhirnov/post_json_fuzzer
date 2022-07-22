import pytest

from src.core.combinator import Combinator
from src.datastructures.metadata import Metadata


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
    def test_take_curr_and_others_by_def(self, metadata_bundle: list, expected_result):
        c = Combinator(metadata_bundle)
        assert c.take_curr_and_others_by_def(metadata_bundle) == expected_result

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
    def test_make_pair_wise(self, metadata_bundle: list, expected_result):
        c = Combinator(metadata_bundle)
        assert c.make_pair_wise(metadata_bundle) == expected_result

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
    def test_make_all_combinations(self, metadata_bundle: list, expected_result):
        c = Combinator(metadata_bundle)
        assert c.make_all_combinations(metadata_bundle) == expected_result

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
                        Metadata("c972b612-df65-4d99-923b-8494d88b0ac6", 1, [200]),
                    ],
            ),
        ],
    )
    def test_miss_it(self, metadata_bundle: list, expected_result):
        c = Combinator(metadata_bundle)
        miss_it_bundle = c.miss_it(metadata_bundle)
        assert miss_it_bundle == expected_result
        assert all([x.fuzz_data is None and x.enabled is False for x in miss_it_bundle])

    @pytest.mark.parametrize(
        "metadata_bundle, expected_result",
        [
            (
                    {
                        1 << 7: [
                            [Metadata("c972b612-df65-4d99-923b-8494d88b0ac1", 1, [200])],
                            [Metadata("c972b612-df65-4d99-923b-8494d88b0ac2", 2, [200])],
                        ],
                        1 << 4: [
                            [Metadata("c972b612-df65-4d99-923b-8494d88b0ac3", 3, [200])],
                            [Metadata("c972b612-df65-4d99-923b-8494d88b0ac4", 4, [200])],
                        ],
                    },
                    [
                        [Metadata("c972b612-df65-4d99-923b-8494d88b0ac1", 1, [200]), Metadata("c972b612-df65-4d99-923b-8494d88b0ac3", 3, [200])],
                        [Metadata("c972b612-df65-4d99-923b-8494d88b0ac1", 1, [200]), Metadata("c972b612-df65-4d99-923b-8494d88b0ac4", 4, [200])],
                        [Metadata("c972b612-df65-4d99-923b-8494d88b0ac2", 2, [200]), Metadata("c972b612-df65-4d99-923b-8494d88b0ac3", 3, [200])],
                        [Metadata("c972b612-df65-4d99-923b-8494d88b0ac2", 2, [200]), Metadata("c972b612-df65-4d99-923b-8494d88b0ac4", 4, [200])]
                     ],
            ),
        ],
    )
    def test_take_curr_and_others_by_their_test_method(self, metadata_bundle: list, expected_result):
        c = Combinator(metadata_bundle)
        assert c.take_curr_and_others_by_their_test_method() == expected_result

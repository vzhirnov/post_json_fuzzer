class TestMethod:
    NUM_OF_TEST_METHODS = 8

    @staticmethod
    def split(tm: int):
        return [
            (1 << x)
            for x in range(0, TestMethod.NUM_OF_TEST_METHODS)
            if ((1 << x) & tm) > 0
        ]

    TAKE_CURR_AND_OTHERS_BY_THEIR_TEST_METHOD = 1 << 7  # DONE
    PAIR_WISE = 1 << 6  # DONE: real PAIR_WISE
    COMBINATIONS = 1 << 5  # DONE: make all COMBINATIONS
    TAKE_CURR_AND_OTHERS_BY_DEF = 1 << 4  # DONE
    NOTHING_MORE_BUT_THIS = 1 << 3
    MISS_IT = 1 << 2  # DONE
    DUPLICATE_IT = (
        1 << 1
    )  # TODO: this is not what we exactly need, json takes just one key and ignore the second one
    HYPOTHESIS = 1 << 0  # TODO: for what??? it seems that it should be deleted

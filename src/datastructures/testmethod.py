class TestMethod:
    NUM_OF_TEST_METHODS = 8

    # TODO make __repr__ view for beauty

    @staticmethod
    def split(tm: int):
        return [
            (1 << x)
            for x in range(0, TestMethod.NUM_OF_TEST_METHODS)
            if ((1 << x) & tm) > 0
        ]

    TAKE_CURR_AND_OTHERS_BY_THEIR_TEST_METHOD = 1 << 7  # 128 DONE
    PAIR_WISE = 1 << 6  # 64 DONE: real PAIR_WISE
    COMBINATIONS = 1 << 5  # 32 DONE: make all COMBINATIONS
    TAKE_CURR_AND_OTHERS_BY_DEF = 1 << 4  # 16 DONE
    NOTHING_MORE_BUT_THIS = 1 << 3  # 8  TODO add only this k_v to json and nothing else
    MISS_IT = 1 << 2  # 4 DONE
    GENERATE_IT = 1 << 1  # 2  # TODO: make generator work for every final json
    HYPOTHESIS = 1 << 0  # 1 TODO: for what??? it seems that it should be deleted

    # def __repr__(self):
    #     return (
    #         f"{self.__class__.__name__}(" f"{self.default_value!r}-{self.obj_id[:6]!r})"
    #     )

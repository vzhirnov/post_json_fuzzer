

class TestMethod:
    num_of_test_methods = 8

    @staticmethod
    def split(tm: int):
        res = []
        for i in range(0, TestMethod.num_of_test_methods):
            val_to_compare = 1 << i
            if (val_to_compare & tm) > 0:
                res.append(val_to_compare)
        return res

    take_curr_and_others_by_their_test_method = 1 << 7  # DONE

    pair_wise = 1 << 6  # DONE: real pair_wise

    combinations = 1 << 5  # DONE: make all combinations

    take_curr_and_others_by_def = 1 << 4  # DONE

    nothing_more_but_this = 1 << 3

    miss_it = 1 << 2  # DONE

    duplicate_it = 1 << 1  # TODO: this is not what we exactly need, json takes just one key and ignore the second one

    hypothesis = 1 << 0  # TODO: for what??? it seems that it should be deleted

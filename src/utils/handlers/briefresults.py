from texttable import Texttable


class ResultsHandlerFactory:
    @classmethod
    def create_handler(cls, actual_results: dict):
        return cls.ResultsHandler(actual_results)


def create_results_handler(factory, actual_results):
    return factory.create_handler(actual_results)


def show_fuzz_results_brief(actual_results: dict, get_replies_with_count):
    print("\nGot the following results:")
    table = Texttable()
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
    table.set_max_width(440)
    titles = ["Deck"]
    rows = []
    results_by_filename = {}

    for relative_file_path, response_data in actual_results.items():
        results_by_filename[relative_file_path] = get_replies_with_count(response_data)

    all_reply_status_reasons = []
    for item in results_by_filename.values():
        for reply_status_reason in item:
            all_reply_status_reasons.append(
                reply_status_reason
            ) if reply_status_reason not in all_reply_status_reasons else True

    for reply_status_reason in all_reply_status_reasons:
        titles.append(" ".join([str(x) for x in reply_status_reason]))

    for relative_file_path, response_data in results_by_filename.items():
        row_to_add = [relative_file_path.name]
        for reply_status in all_reply_status_reasons:
            row_to_add.append(len(response_data.get(reply_status, [])))
        rows.append(row_to_add)

    table.set_header_align(["l" for _ in titles])
    table.set_cols_align(["l" if i == 0 else "r" for i, x in enumerate(titles)])

    table.add_rows([titles, *rows])
    print(table.draw())


class SyncResultsHandlerFactory(ResultsHandlerFactory):
    class ResultsHandler:
        def __init__(self, actual_results: dict):
            self.actual_results = actual_results

        def get_replies_with_count(self, client_responses: list) -> dict:
            replies_with_count = {}
            for response in client_responses:
                if response[3]["suspicious_reply"]:
                    t0 = ("Suspicious", response[0].status_code, response[0].reason)
                    replies_with_count[t0] = (
                        [response[1]]
                        if replies_with_count.get(t0) is None
                        else replies_with_count[t0] + [response[1]]
                    )
                    continue
                t1 = (response[0].status_code, response[0].reason)
                replies_with_count[t1] = (
                    [response[1]]
                    if replies_with_count.get(t1) is None
                    else replies_with_count[t1] + [response[1]]
                )
            return replies_with_count

        def show_fuzz_results_brief(self):
            show_fuzz_results_brief(self.actual_results, self.get_replies_with_count)


class AsyncResultsHandlerFactory(ResultsHandlerFactory):
    class ResultsHandler:
        def __init__(self, actual_results: dict):
            self.actual_results = actual_results

        def get_replies_with_count(self, client_responses: list) -> dict:
            replies_with_count = {}
            for response in client_responses:
                if response[3]["suspicious_reply"]:
                    t0 = ("Suspicious", response[0].status, response[0].reason)
                    replies_with_count[t0] = (
                        [response[1]]
                        if replies_with_count.get(t0) is None
                        else replies_with_count[t0] + [response[1]]
                    )
                    continue
                t1 = (response[0].status, response[0].reason)
                replies_with_count[t1] = (
                    [response[1]]
                    if replies_with_count.get(t1) is None
                    else replies_with_count[t1] + [response[1]]
                )
            return replies_with_count

        def show_fuzz_results_brief(self):
            show_fuzz_results_brief(self.actual_results, self.get_replies_with_count)

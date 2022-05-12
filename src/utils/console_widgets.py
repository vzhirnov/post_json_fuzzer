import glob
import os
from texttable import Texttable
from pathlib import Path

from default_values import DefaultValues


def clear_console():
    os.system("clear")


def add_blank_line():
    print()


def add_line_separator():
    print("#" * 120)


def show_post_json_fuzzer_title():
    print("POST-JSON-FUZZER v2.0.0")


def show_start_fuzz_info(route: str, headers, file_or_dir):
    print("Route:")
    print(f"\t{route}")

    print("Custom headers:")
    for header in headers:
        print(f"\t{header}")
    print("Cartridges with fuzzies to handle:")

    if Path(file_or_dir).is_dir():
        folder = Path(file_or_dir)
        path = os.path.join(
            folder.absolute(), "*" + DefaultValues.FUZZIES_EXTENSION
        )  # TODO get rid of os.path
        if folder.is_dir():
            for file_name in glob.glob(path):
                print(f"\t{Path(file_name).stem}")


def show_fuzz_results_brief(actual_results: dict):
    print("\nGot the following results:")
    table = Texttable()
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
    table.set_max_width(440)
    titles = ["Cartridge"]
    rows = []
    results_by_filename = {}

    def get_replies_with_count(client_responses: list) -> dict:
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

    table.set_header_align(["l" for x in titles])
    table.set_cols_align(["l" if i == 0 else "r" for i, x in enumerate(titles)])

    table.add_rows([titles, *rows])
    print(table.draw())

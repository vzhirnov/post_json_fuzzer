from texttable import Texttable
import os


def clear_console():
    os.system('clear')


def add_line_separator():
    print("#" * 120)


def show_post_json_fuzzer_title():
    print("POST-JSON-FUZZER v2.0.0")


def show_start_fuzz_info(route: str, headers, files_to_handle):
    if isinstance(files_to_handle, str):
        files_to_handle = [files_to_handle]
    if isinstance(headers, str):
        headers = [headers]

    print("Route:")
    print(f"\t{route}")

    print("Custom headers:")
    for header in headers:
        print(f"\t{header}")
    print("Cartridges with fuzzies to handle:")
    for file in files_to_handle:
        print(f"\t{file}")


def show_fuzz_results_brief(file: str, actual_results: dict):
    print("\nGot the following results:")
    table = Texttable()
    table.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)
    table.set_max_width(440)
    titles = ["Cartridge"]
    res = [file]
    for key, value in actual_results.items():
        titles.append(" ".join([str(x) for x in key]))
        res.append(len(actual_results[key]))

    table.set_header_align(["l" for x in titles])
    table.set_cols_align(["l" if i == 0 else "r" for i, x in enumerate(res)])

    table.add_rows([titles, res])
    print(table.draw())

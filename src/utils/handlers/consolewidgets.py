import glob
import os
from pathlib import Path

from defaults.constants import ProjectValues


def clear_console():
    os.system("clear")


def add_blank_line():
    print()


def add_line_separator():
    print("#" * 120)


def show_post_json_fuzzer_title():
    print("POST-JSON-FUZZER v2.1.1")


def show_start_fuzz_info(route: str, headers: dict, file_or_dir: str):
    print("Route:")
    print(f"\t{route}")

    print("Custom headers:")
    for header in headers:
        print(f"\t{header}")
    print("Decks with fuzzies to handle:")

    if Path(file_or_dir).is_dir():
        folder = Path(file_or_dir)
        path = os.path.join(
            folder.absolute(), "*" + ProjectValues.FUZZIES_EXTENSION
        )  # TODO get rid of os.path
        if folder.is_dir():
            for file_name in glob.glob(path):
                print(f"\t{Path(file_name).stem}")
    elif Path(file_or_dir).is_file():
        print(f"\t{Path(file_or_dir).stem}")



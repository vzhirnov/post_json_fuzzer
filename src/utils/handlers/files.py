import glob
import os

from defaults.constants import ProjectValues
from pathlib import Path

from src.datastructures.fuzzy import Fuzzy
from src.datastructures.testmethod import TestMethod as tm
from src.strategies.aggregator import *


def get_filename(param):
    return Path(param).stem


def make_dir(dir_name: str) -> bool:
    try:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def load_deck_from_file(file_name: str) -> dict:
    deck_bundle = {}
    file = Path(file_name)
    if file.is_file():
        base_name = file.name
        if Path(base_name).suffix == ProjectValues.FUZZIES_EXTENSION:
            with open(file_name, "rb") as f:
                try:
                    deck_bundle[file] = eval(f.read())
                except Exception:
                    raise Exception(
                        f"Error: cannot make eval method for {get_filename(file_name)}"
                    )
    return deck_bundle


def load_decks_from_folder(dir_name: str) -> dict:
    deck_bundle = {}
    folder = Path(dir_name)
    if folder.is_dir():
        for file_name in glob.glob(
            os.path.join(folder.absolute(), "*" + ProjectValues.FUZZIES_EXTENSION)
        ):
            with open(file_name, "r") as f:
                try:
                    base_name = Path(file_name).name
                    deck_bundle[folder / base_name] = eval(f.read())
                except Exception:
                    raise Exception(
                        f"Error: cannot make eval method for {get_filename(file_name)}"
                    )
    return deck_bundle

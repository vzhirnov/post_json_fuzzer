import os
from pathlib import Path


class DefaultValues:
    PROJECT_ROOT_DIR = Path.cwd()
    RESULTS_ROOT_DIR = PROJECT_ROOT_DIR / "results"
    CARTRIDGES_DIR = PROJECT_ROOT_DIR / "cartridges"

    FUZZIES_EXTENSION = ".deck"

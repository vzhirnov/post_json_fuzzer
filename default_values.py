from pathlib import Path


class DefaultValues:
    PROJECT_ROOT_DIR = Path.cwd()
    RESULTS_ROOT_DIR = PROJECT_ROOT_DIR / "results"
    DECKS_DIR = PROJECT_ROOT_DIR / "decks"

    FUZZIES_EXTENSION = ".deck"

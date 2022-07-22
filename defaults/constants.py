from pathlib import Path


class ProjectValues:
    ROOT_DIR = Path.cwd()
    RESULTS_ROOT_DIR = ROOT_DIR / "results"
    DECKS_DIR = ROOT_DIR / "decks"

    FUZZIES_EXTENSION = ".deck"

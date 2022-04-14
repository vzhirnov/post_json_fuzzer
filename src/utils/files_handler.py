from pathlib import Path


def get_filename(param):
    return Path(param).stem

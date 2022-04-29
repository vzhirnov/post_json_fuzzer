import pathlib


def get_filename(param):
    return pathlib.Path(param).stem


def make_dir(dir_name: str) -> bool:
    try:
        pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

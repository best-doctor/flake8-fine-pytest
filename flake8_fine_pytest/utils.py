import pathlib


def get_stem(filepath: str | pathlib.Path) -> str:
    return pathlib.PurePath(filepath).stem

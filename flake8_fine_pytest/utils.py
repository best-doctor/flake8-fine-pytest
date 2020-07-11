import pathlib
from typing import Union


def get_stem(filepath: Union[str, pathlib.Path]) -> str:
    return pathlib.PurePath(filepath).stem

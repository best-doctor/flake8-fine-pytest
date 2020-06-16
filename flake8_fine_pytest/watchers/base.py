import ast
from typing import List

from flake8.options.manager import OptionManager

from flake8_fine_pytest.common_types import ErrorType


class BaseWatcher:
    def __init__(self, options: OptionManager, filename: str, tree: ast.AST) -> None:
        self.options = options
        self.filename = filename
        self.tree = tree

        self.errors: List[ErrorType] = []

    def add_error(self, error: ErrorType) -> None:
        self.errors.append(error)

    def run(self) -> None:
        pass

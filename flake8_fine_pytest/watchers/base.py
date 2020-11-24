import ast
from typing import List

from flake8.options.manager import OptionManager

from flake8_fine_pytest.common_types import ErrorType
from flake8_fine_pytest.utils import get_stem


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

    def _is_test_file(self, filename: str) -> bool:
        stem = get_stem(self.filename)
        return stem.startswith('test_')

    def _is_test_function(self, node: ast.AST) -> bool:
        return isinstance(node, ast.FunctionDef) and node.name.startswith('test_')

    def _should_run(self) -> bool:
        return self._is_test_file(self.filename)

    def _should_check_node(self, node: ast.AST) -> bool:
        return self._is_test_function(node)

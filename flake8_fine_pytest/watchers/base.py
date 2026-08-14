import ast

from flake8_fine_pytest.common_types import AnyFunctionDef, ErrorType, Options
from flake8_fine_pytest.utils import get_stem

FUNCTION_DEF_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)


class BaseWatcher:
    config_option = ''

    def __init__(self, options: Options, filename: str, tree: ast.AST) -> None:
        self.options = options
        self.filename = filename
        self.tree = tree

        self.errors: list[ErrorType] = []

    def add_error(self, error: ErrorType) -> None:
        self.errors.append(error)

    def run(self) -> None:
        raise NotImplementedError

    def should_run(self) -> bool:
        return (
            self._is_test_file()
            and bool(getattr(self.options, self.config_option))
        )

    def _is_test_file(self) -> bool:
        return get_stem(self.filename).startswith('test_')

    def _is_test_function(self, node: ast.AST) -> bool:
        return isinstance(node, FUNCTION_DEF_NODES) and node.name.startswith('test_')

    def _should_check_node(self, node: ast.AST) -> bool:
        return self._is_test_function(node)

    def _iterate_over_test_functions(self, tree: ast.AST) -> list[AnyFunctionDef]:
        return [node for node in ast.walk(tree) if self._is_test_function(node)]  # type: ignore[misc]

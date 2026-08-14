import ast
from collections.abc import Iterator

from flake8_fine_pytest.common_types import AnyFunctionDef
from flake8_fine_pytest.watchers.base import BaseWatcher


def is_static_method(node: AnyFunctionDef) -> bool:
    return any(
        isinstance(decorator, ast.Name) and decorator.id == 'staticmethod'
        for decorator in node.decorator_list
    )


class UsefixturesWatcher(BaseWatcher):
    config_option = 'force_usefixtures'
    error_template = (
        'FP010 {test_name} should use fixtures as follows: '
        '@pytest.mark.usefixtures({fixtures_list_as_str})'
    )

    def run(self) -> None:
        for test_node, is_class_member in self._iterate_over_test_function_definitions():
            fixture_names = self._get_unreferenced_fixture_names(test_node, is_class_member)
            if fixture_names:
                self._add_usefixtures_error(test_node, fixture_names)

    def _iterate_over_test_function_definitions(self) -> Iterator[tuple[AnyFunctionDef, bool]]:
        """
        Returns any FunctionDef that looks like a test.

        As pytest only discovers first-level-of-nesting tests, we only yield
        top-level function definitions and top-level classes method definitions.
        """
        for node in ast.iter_child_nodes(self.tree):
            if self._should_check_node(node):
                yield node, False  # type: ignore[misc]

            elif isinstance(node, ast.ClassDef) and node.name.startswith(('Test', 'test')):
                yield from self._iterate_over_test_class_nodes(node)

    def _iterate_over_test_class_nodes(
        self, class_node: ast.ClassDef,
    ) -> Iterator[tuple[AnyFunctionDef, bool]]:
        for node in ast.iter_child_nodes(class_node):
            if self._should_check_node(node):
                yield node, True  # type: ignore[misc]

    def _get_unreferenced_fixture_names(
        self, function_node: AnyFunctionDef, is_class_method: bool,
    ) -> list[str]:
        referenced_variable_names = {
            node.id
            for node in ast.walk(function_node)
            if isinstance(node, ast.Name)
        }

        if is_class_method and not is_static_method(function_node):
            # `self` or `cls`, or whatever it happens to be called.
            positional_arguments = function_node.args.args
            if positional_arguments:
                referenced_variable_names.add(positional_arguments[0].arg)

        test_fixture_names = {arg.arg for arg in function_node.args.args}

        return sorted(test_fixture_names - referenced_variable_names)

    def _add_usefixtures_error(
        self, function_node: AnyFunctionDef, fixture_names: list[str],
    ) -> None:
        error_message = self.error_template.format(
            test_name=function_node.name,
            fixtures_list_as_str=', '.join(repr(name) for name in fixture_names),
        )
        self.add_error((function_node.lineno, 0, error_message))

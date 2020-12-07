import ast

from flake8_fine_pytest.watchers.base import BaseWatcher


class AssertCountWatcher(BaseWatcher):
    config_option = 'allowed_assert_count'
    error_template = (
        'FP005 {test_name} has too many assert statements. '
        'Allowed count of asserts is {allowed_assert_count}'
    )

    def run(self) -> None:
        self.allowed_assert_count = self.options.allowed_assert_count
        self._validate_assert_count(self.tree)

    def _validate_assert_count(self, tree: ast.AST) -> None:
        for node in ast.walk(tree):
            if self._should_check_node(node) is False:
                continue

            if self._is_valid(node) is False:  # type: ignore
                self._note_an_error(node)

    def _is_valid(self, node: ast.FunctionDef) -> bool:
        asserts_count = self._get_actual_asserts_count(node)

        return self.allowed_assert_count >= asserts_count

    def _get_actual_asserts_count(self, node: ast.FunctionDef) -> int:
        asserts_count = 0

        for body_element in node.body:
            if isinstance(body_element, ast.Assert):
                asserts_count += 1

        return asserts_count

    def _note_an_error(self, node: ast.AST) -> None:
        error_message = self._get_error_message(node)  # type: ignore
        self.add_error((node.lineno, 0, error_message))

    def _get_error_message(self, node: ast.FunctionDef) -> str:
        invalid_test_name = node.name

        return self.error_template.format(
            test_name=invalid_test_name, allowed_assert_count=self.allowed_assert_count,
        )

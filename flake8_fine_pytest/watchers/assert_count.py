import ast

from flake8_fine_pytest.common_types import AnyFunctionDef
from flake8_fine_pytest.watchers.base import BaseWatcher


class AssertCountWatcher(BaseWatcher):
    config_option = 'allowed_assert_count'
    error_template = (
        'FP005 {test_name} has too many assert statements. '
        'Allowed count of asserts is {allowed_assert_count}'
    )

    def run(self) -> None:
        allowed_assert_count = self.options.allowed_assert_count

        for node in self._iterate_over_test_functions(self.tree):
            if self._get_actual_asserts_count(node) > allowed_assert_count:
                self._note_an_error(node, allowed_assert_count)

    def _get_actual_asserts_count(self, node: AnyFunctionDef) -> int:
        return sum(isinstance(body_element, ast.Assert) for body_element in node.body)

    def _note_an_error(self, node: AnyFunctionDef, allowed_assert_count: int) -> None:
        error_message = self.error_template.format(
            test_name=node.name, allowed_assert_count=allowed_assert_count,
        )
        self.add_error((node.lineno, 0, error_message))

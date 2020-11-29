import ast
from typing import Set

from flake8_fine_pytest.watchers.base import BaseWatcher


class UniqueTestNamesWatcher(BaseWatcher):
    error_template = 'FP009 Duplicate name test case ({})'

    def run(self) -> None:
        testcases_names: Set[str] = set()

        if not self._is_test_file(self.filename):
            return

        for node in ast.walk(self.tree):
            if not self._should_check_node(node):
                continue

            node_name = node.name  # type: ignore

            if node_name not in testcases_names:
                testcases_names.add(node_name)
                continue

            error_msg = self.error_template.format(node_name)
            self.add_error((node.lineno, 0, error_msg))

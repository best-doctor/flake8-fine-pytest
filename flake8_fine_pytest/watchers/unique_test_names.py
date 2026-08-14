from flake8_fine_pytest.watchers.base import BaseWatcher


class UniqueTestNamesWatcher(BaseWatcher):
    config_option = 'force_unique_test_names'
    error_template = 'FP009 Duplicate name test case ({test_name})'

    def run(self) -> None:
        seen_testcase_names: set[str] = set()

        for node in self._iterate_over_test_functions(self.tree):
            if node.name in seen_testcase_names:
                error_message = self.error_template.format(test_name=node.name)
                self.add_error((node.lineno, 0, error_message))
            else:
                seen_testcase_names.add(node.name)

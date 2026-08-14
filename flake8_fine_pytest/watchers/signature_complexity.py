from flake8_fine_pytest.common_types import AnyFunctionDef
from flake8_fine_pytest.watchers.base import BaseWatcher


class SignatureComplexityWatcher(BaseWatcher):
    config_option = 'allowed_test_arguments_count'
    error_template = (
        'FP004 {test_name} has too complex signature. '
        'Allowed count of arguments is {allowed_arguments}'
    )

    def run(self) -> None:
        allowed_test_arguments_count = self.options.allowed_test_arguments_count

        for node in self._iterate_over_test_functions(self.tree):
            if len(node.args.args) > allowed_test_arguments_count:
                self._note_an_error(node, allowed_test_arguments_count)

    def _note_an_error(self, node: AnyFunctionDef, allowed_arguments: int) -> None:
        error_message = self.error_template.format(
            test_name=node.name, allowed_arguments=allowed_arguments,
        )
        self.add_error((node.lineno, 0, error_message))

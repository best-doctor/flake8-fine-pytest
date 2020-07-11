import ast

from flake8_fine_pytest.watchers.base import BaseWatcher


class SignatureComplexityWatcher(BaseWatcher):
    error_template = (
        'FP004 {test_name} has too complex signature. '
        'Allowed count of arguments is {allowed_arguments}'
    )

    def run(self) -> None:
        self.allowed_test_arguments_count = self.options.allowed_test_arguments_count

        if self._should_check():
            self._validate_signature_arguments_count(self.tree)

    def _should_check(self) -> bool:
        return self._is_test_file(self.filename) and self.allowed_test_arguments_count is not None

    def _validate_signature_arguments_count(self, tree: ast.AST) -> None:
        for node in ast.walk(tree):
            if self._is_properly_node(node) is False:
                continue

            if self._is_invalid_signature(node) is True:  # type: ignore
                self._note_an_error(node)

    def _is_properly_node(self, node: ast.AST) -> bool:
        return isinstance(node, ast.FunctionDef) and node.name.startswith('test_')

    def _is_invalid_signature(self, ast_node: ast.FunctionDef) -> bool:
        signature_arguments = ast_node.args.args

        return len(signature_arguments) > self.allowed_test_arguments_count

    def _note_an_error(self, node: ast.AST) -> None:
        error_message = self._get_error_message(node)  # type: ignore
        self.add_error((node.lineno, 0, error_message))

    def _get_error_message(self, node: ast.FunctionDef) -> str:
        invalid_test_name = node.name

        return self.error_template.format(
            test_name=invalid_test_name, allowed_arguments=self.allowed_test_arguments_count,
        )

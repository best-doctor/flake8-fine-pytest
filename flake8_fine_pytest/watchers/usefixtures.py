import ast
import typing

from flake8_fine_pytest.watchers.base import BaseWatcher


class UsefixturesWatcher(BaseWatcher):
    error_template = (
        'FP009 {test_name} should use fixtures as follows: '
        '@pytest.mark.usefixtures({fixtures_list_as_str})'
    )

    def run(self) -> None:
        if self._should_run():
            self._validate_usefixtures_used_where_possible(self.tree)

    def _should_run(self) -> bool:
        return self.options.force_usefixtures and super()._should_run()

    def _validate_usefixtures_used_where_possible(self, tree: ast.AST) -> None:
        for node in ast.walk(tree):
            if not self._should_check_node(node):
                continue

            fixture_names = self._get_unreferenced_fixture_names(node)  # type: ignore
            if fixture_names:
                self._add_usefixtures_error(node, fixture_names)  # type: ignore

    def _get_unreferenced_fixture_names(
        self,
        function_node: ast.FunctionDef,
    ) -> typing.List[str]:
        referenced_variable_names = {
            node.id
            for node in ast.walk(function_node)
            if isinstance(node, ast.Name)
        }
        test_fixture_names = {arg.arg for arg in function_node.args.args}

        return sorted(test_fixture_names - referenced_variable_names)

    def _add_usefixtures_error(
        self,
        function_node: ast.FunctionDef,
        fixture_names: typing.List[str],
    ) -> None:
        error_message = self.error_template.format(
            test_name=function_node.name,
            fixtures_list_as_str=', '.join(repr(name) for name in fixture_names),
        )
        self.add_error((function_node.lineno, 0, error_message))

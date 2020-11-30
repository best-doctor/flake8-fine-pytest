import ast
import typing

from flake8_fine_pytest.watchers.base import BaseWatcher


def is_static_method(node: ast.FunctionDef) -> bool:
    for decorator in node.decorator_list:
        if isinstance(decorator, ast.Name) and decorator.id == 'staticmethod':
            return True


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
        for test_node, is_class_member in self._iterate_over_test_function_definitions(tree):
            fixture_names = self._get_unreferenced_fixture_names(
                test_node, is_class_member,
            )
            if fixture_names:
                self._add_usefixtures_error(test_node, fixture_names)

    def _iterate_over_test_function_definitions(
        self, tree: ast.AST,
    ) -> typing.Iterator[typing.Tuple[ast.FunctionDef, bool]]:
        """
        Returns any FunctionDef that looks like a test.

        As pytest only discovers first-level-of-nesting tests, we only yield
        top-level function definitions and top-level classes method definitions.
        """
        for node in ast.iter_child_nodes(self.tree):
            if self._should_check_node(node):
                yield node, False  # type: ignore

            elif(
                isinstance(node, ast.ClassDef)
                and node.name.startswith(('Test', 'test'))
            ):
                yield from self._iterate_over_test_class_nodes(node)

    def _iterate_over_test_class_nodes(
        self, class_node: ast.AST,
    ) -> typing.Iterator[typing.Tuple[ast.FunctionDef, bool]]:
        for node in ast.iter_child_nodes(class_node):
            if self._should_check_node(node):
                yield node, True  # type: ignore

    def _get_unreferenced_fixture_names(
        self,
        function_node: ast.FunctionDef,
        is_class_method: bool,
    ) -> typing.List[str]:
        referenced_variable_names = {
            node.id
            for node in ast.walk(function_node)
            if isinstance(node, ast.Name)
        }

        if is_class_method and not is_static_method(function_node):
            try:
                # `self` or `cls`, or whatever it happens to be called.
                referenced_variable_names.add(function_node.args.args[0].arg)
            except IndexError:
                # wrong class method definition. Skip silently.
                pass

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

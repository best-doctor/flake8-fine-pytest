import ast
from datetime import date
from typing import List, Any, Optional

from flake8_fine_pytest.watchers.base import BaseWatcher


class XfailUntilArgumentHasCorrectFormatValidator:
    error_template = (
        'FP007 xfail mark has wrong format. It should has `until` argument with datetime.date type'
    )

    @classmethod
    def validate(cls, until_decorator_keyword: ast.keyword) -> str:
        until_args_object = until_decorator_keyword.value

        if isinstance(until_args_object, ast.Call) is False:
            return cls.error_template


class XfailUntilArgumentFreshEnoughValidator:
    error_template = (
        'FP008 stale xfail mark'
    )

    @classmethod
    def _get_xfail_until_date_with_backward_compatibility(cls, until_date_object_args: Any) -> date:
        """
        Parses until date constants.

        We need this because of ast.Num deprecation from python3.8
        https://greentreesnakes.readthedocs.io/en/latest/nodes.html#Num
        """
        year_node, month_node, day_node = until_date_object_args

        if isinstance(year_node, ast.Num):
            return date(year_node.n, month_node.n, day_node.n)  # type: ignore

        if isinstance(year_node, ast.Constant):
            return date(year_node.value, month_node.value, day_node.value)

    @classmethod
    def validate(cls, until_decorator_keyword: ast.keyword) -> Optional[str]:
        until_args_object = until_decorator_keyword.value

        if isinstance(until_args_object, ast.Call) is False:
            return None

        until_date = cls._get_xfail_until_date_with_backward_compatibility(until_args_object.args)  # type: ignore

        if date.today() > until_date:
            return cls.error_template


class XfailUntilArgumentWatcher(BaseWatcher):
    error_template = (
        'FP006 xfail mark has wrong format. It should has `until` argument'
    )
    required_xfail_until_argument_name = 'until'
    validators = [
        XfailUntilArgumentHasCorrectFormatValidator,
        XfailUntilArgumentFreshEnoughValidator,
    ]

    def run(self) -> None:
        if self._should_check():
            self._find_decorators_node_to_validate()

    def _should_check(self) -> bool:
        return self._is_test_file(self.filename)

    def _is_xfail_call(self, decorator: ast.Call) -> bool:
        return (
            hasattr(decorator, 'func')
            and hasattr(decorator.func, 'attr')
            and decorator.func.attr == 'xfail'  # type: ignore
        )

    def _find_decorators_node_to_validate(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                decorators = node.decorator_list

                self._validate_decorators(decorators)  # type: ignore

    def _validate_decorators(self, decorators: List[ast.Call]) -> None:
        for decorator in decorators:
            if self._is_xfail_call(decorator) is False:
                continue

            self._validate_xfail_decorator_args(decorator)

    def _validate_xfail_decorator_args(self, decorator: ast.Call) -> None:
        xfail_args = [
            keyword.arg for keyword in decorator.keywords if hasattr(keyword, 'arg')
        ]

        if self.required_xfail_until_argument_name not in xfail_args:
            return self.add_error((decorator.lineno, 0, self.error_template))

        for keyword in decorator.keywords:
            if keyword.arg == self.required_xfail_until_argument_name:
                return self._validate_xfail_decorator_until_argument(decorator, keyword)

    def _validate_xfail_decorator_until_argument(self, decorator: ast.Call, until_keyword: ast.keyword) -> None:
        for validator in self.validators:
            error = validator.validate(until_keyword)  # type: ignore

            if error:
                return self.add_error((decorator.lineno, 0, error))

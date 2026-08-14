import ast
from datetime import date

from flake8_fine_pytest.ast_helpers import is_xfail_mark
from flake8_fine_pytest.watchers.base import FUNCTION_DEF_NODES, BaseWatcher

DATE_FIELD_NAMES = ('year', 'month', 'day')


def _resolve_date_arguments(call: ast.Call) -> list[object] | None:
    """Maps a `date()` call onto its year, month and day literal values."""
    keywords = {keyword.arg: keyword.value for keyword in call.keywords}

    argument_nodes: list[ast.expr | None] = list(call.args)
    argument_nodes.extend(
        keywords.get(name) for name in DATE_FIELD_NAMES[len(argument_nodes):]
    )

    if len(argument_nodes) != len(DATE_FIELD_NAMES):
        return None

    if not all(isinstance(node, ast.Constant) for node in argument_nodes):
        return None

    return [node.value for node in argument_nodes]  # type: ignore[union-attr]


def parse_date_call(node: ast.expr) -> date | None:
    """
    Builds a date out of a literal `date(year, month, day)` call.

    Both positional and keyword arguments are understood. Returns None whenever
    the call cannot be resolved statically, e.g. when its arguments are names or
    expressions rather than plain number literals.
    """
    if not isinstance(node, ast.Call):
        return None

    arguments = _resolve_date_arguments(node)
    if arguments is None:
        return None

    try:
        return date(*arguments)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


class XfailUntilArgumentHasCorrectFormatValidator:
    error_template = (
        'FP007 xfail mark has wrong format. It should has `until` argument with datetime.date type'
    )

    @classmethod
    def validate(cls, until_decorator_keyword: ast.keyword) -> str | None:
        if not isinstance(until_decorator_keyword.value, ast.Call):
            return cls.error_template
        return None


class XfailUntilArgumentFreshEnoughValidator:
    error_template = 'FP008 stale xfail mark'

    @classmethod
    def validate(cls, until_decorator_keyword: ast.keyword) -> str | None:
        until_date = parse_date_call(until_decorator_keyword.value)

        if until_date is not None and date.today() > until_date:
            return cls.error_template
        return None


class XfailUntilArgumentWatcher(BaseWatcher):
    config_option = 'xfail_check_until'
    error_template = 'FP006 xfail mark has wrong format. It should has `until` argument'
    required_xfail_until_argument_name = 'until'
    validators = (
        XfailUntilArgumentHasCorrectFormatValidator,
        XfailUntilArgumentFreshEnoughValidator,
    )

    def run(self) -> None:
        for node in ast.walk(self.tree):
            if isinstance(node, FUNCTION_DEF_NODES):
                self._validate_decorators(node.decorator_list)

    def _is_xfail_decorator(self, decorator: ast.expr) -> bool:
        return isinstance(decorator, ast.Call) and is_xfail_mark(decorator.func)

    def _validate_decorators(self, decorators: list[ast.expr]) -> None:
        for decorator in decorators:
            if self._is_xfail_decorator(decorator):
                self._validate_xfail_decorator_args(decorator)  # type: ignore[arg-type]

    def _validate_xfail_decorator_args(self, decorator: ast.Call) -> None:
        for keyword in decorator.keywords:
            if keyword.arg == self.required_xfail_until_argument_name:
                self._validate_xfail_decorator_until_argument(decorator, keyword)
                return

        self.add_error((decorator.lineno, 0, self.error_template))

    def _validate_xfail_decorator_until_argument(
        self, decorator: ast.Call, until_keyword: ast.keyword,
    ) -> None:
        for validator in self.validators:
            error = validator.validate(until_keyword)

            if error:
                self.add_error((decorator.lineno, 0, error))
                return

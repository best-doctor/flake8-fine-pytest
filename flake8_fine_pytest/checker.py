import ast
import typing
from flake8_fine_pytest import __version__ as version

from flake8_fine_pytest.ast_helpers import get_wrong_xfail_decorator_lines

ErrorType = typing.Tuple[int, int, str, type]


class FinePytestChecker:
    name = 'flake8-fine-pytest'
    version = version

    def __init__(self, tree: ast.AST, filename: str):
        self.filename = filename
        self.tree = tree

    def run(self) -> typing.Generator[ErrorType, None, None]:
        xfail_with_empty_reason, xfail_without_reason = get_wrong_xfail_decorator_lines(self.tree)
        errors = self.get_xfail_reason_errors(
            xfail_with_empty_reason,
            xfail_without_reason,
        )
        for error in errors:
            yield (*error, type(self))

    def get_xfail_reason_errors(
        self,
        xfail_with_empty_reason: typing.Set[int],
        xfail_without_reason: typing.Set[int],
    ) -> typing.List[typing.Tuple[int, int, str]]:
        errors = []
        if xfail_with_empty_reason or xfail_without_reason:

            for line in xfail_with_empty_reason:
                errors.append((
                    line,
                    0,
                    'FP001 xfailed test with empty reason'
                ))
            for line in xfail_without_reason:
                errors.append((
                    line,
                    0,
                    'FP002 xfailed test without reason'
                ))
        return errors

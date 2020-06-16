from typing import Set

from flake8_fine_pytest.watchers.base import BaseWatcher
from flake8_fine_pytest.ast_helpers import get_wrong_xfail_decorator_lines


class XfailWatcher(BaseWatcher):
    def run(self) -> None:
        xfail_with_empty_reason, xfail_without_reason = get_wrong_xfail_decorator_lines(self.tree)

        if xfail_with_empty_reason or xfail_without_reason:
            self._collect_absent_reason_errors(xfail_without_reason)
            self._collect_empty_reason_errors(xfail_with_empty_reason)

    def _collect_empty_reason_errors(self, xfail_with_empty_reason: Set) -> None:
        for line in xfail_with_empty_reason:
            self.add_error((
                line,
                0,
                'FP001 xfailed test with empty reason',
            ))

    def _collect_absent_reason_errors(self, xfail_without_reason: Set) -> None:
        for line in xfail_without_reason:
            self.add_error((
                line,
                0,
                'FP002 xfailed test without reason',
            ))

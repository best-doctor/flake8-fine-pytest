import ast

from flake8.options.manager import OptionManager

from flake8_fine_pytest import __version__ as version
from flake8_fine_pytest.watchers.modules_structure import ModulesStructureWatcher
from flake8_fine_pytest.watchers.unique_test_names import UniqueTestNamesWatcher
from flake8_fine_pytest.watchers.xfail_decorator import XfailWatcher
from flake8_fine_pytest.watchers.xfail_until_argument_watcher import (
    XfailUntilArgumentWatcher,
)
from flake8_fine_pytest.watchers.signature_complexity import SignatureComplexityWatcher
from flake8_fine_pytest.watchers.assert_count import AssertCountWatcher
from flake8_fine_pytest.watchers.usefixtures import UsefixturesWatcher
from flake8_fine_pytest.common_types import CheckResult


class FinePytestChecker:
    name = 'flake8-fine-pytest'
    version = version
    options = None

    _watchers = (
        XfailWatcher,
        ModulesStructureWatcher,
        SignatureComplexityWatcher,
        AssertCountWatcher,
        XfailUntilArgumentWatcher,
        UsefixturesWatcher,
        UniqueTestNamesWatcher,
    )

    def __init__(self, tree: ast.AST, filename: str):
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        parser.add_option(
            '--allowed-test-directories',
            comma_separated_list=True,
            parse_from_config=True,
            default=['test_unit', 'test_integration'],
            help='Comma-separated list of allowed test directories',
        )
        parser.add_option(
            '--allowed-test-arguments-count',
            type=int,
            parse_from_config=True,
            default=6,
            help='Allowed arguments in test signature',
        )
        parser.add_option(
            '--allowed-assert-count',
            type=int,
            parse_from_config=True,
            default=6,
            help='Allowed assert statement count in test',
        )
        parser.add_option(
            '--xfail-check-until',
            action='store_true',
            default=True,
            parse_from_config=True,
            help='Check that xfail has until parameter',
        )
        parser.add_option(
            '--xfail-check-reason',
            action='store_true',
            default=True,
            parse_from_config=True,
            help='Check that xfail has reason parameter',
        )
        parser.add_option(
            '--force-unique-test-names',
            action='store_true',
            parse_from_config=True,
            default=True,
            help='Enforce unqiue test names',
        )
        parser.add_option(
            '--force-usefixtures',
            action='store_true',
            parse_from_config=True,
            default=True,
            help='Enforce usefixtures validator',
        )

    @classmethod
    def parse_options(cls, options: str) -> None:
        cls.options = options

    def run(self) -> CheckResult:
        for watcher_class in self._watchers:
            watcher = watcher_class(self.options, self.filename, self.tree)

            if watcher.should_run():
                watcher.run()

            yield from (  # type: ignore
                (*error, type(self))
                for error in watcher.errors
            )

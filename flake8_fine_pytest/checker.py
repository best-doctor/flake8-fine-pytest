import ast

from flake8.options.manager import OptionManager

from flake8_fine_pytest import __version__ as version
from flake8_fine_pytest.watchers.modules_structure import ModulesStructureWatcher
from flake8_fine_pytest.watchers.xfail_decorator import XfailWatcher
from flake8_fine_pytest.watchers.signature_complexity import SignatureComplexityWatcher
from flake8_fine_pytest.common_types import CheckResult


class FinePytestChecker:
    name = 'flake8-fine-pytest'
    version = version
    options = None

    _watchers = (
        XfailWatcher,
        ModulesStructureWatcher,
        SignatureComplexityWatcher,
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
            help='Comma-separated list of allowed test directories',
        )
        parser.add_option(
            '--allowed-test-arguments-count',
            parse_from_config=True,
            help='Allowed arguments in test signature',
        )

    @classmethod
    def parse_options(cls, options: str) -> None:
        cls.options = options

    def run(self) -> CheckResult:
        for watcher_class in self._watchers:
            watcher = watcher_class(self.options, self.filename, self.tree)

            watcher.run()

            yield from (  # type: ignore
                (*error, type(self))
                for error in watcher.errors
            )

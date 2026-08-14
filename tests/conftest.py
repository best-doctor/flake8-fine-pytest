import argparse
import ast
import pathlib
from collections.abc import Callable

import pytest

from flake8_fine_pytest.checker import FinePytestChecker

TEST_FILES_DIR = pathlib.Path(__file__).parent / 'test_files'

DISABLED_OPTIONS = {
    'allowed_test_directories': None,
    'allowed_test_arguments_count': None,
    'allowed_assert_count': None,
    'xfail_check_until': False,
    'xfail_check_reason': False,
    'force_unique_test_names': False,
    'force_usefixtures': False,
}


def build_options(**overrides: object) -> argparse.Namespace:
    """Builds the options namespace flake8 hands over to the checker."""
    unknown_options = set(overrides) - set(DISABLED_OPTIONS)
    if unknown_options:
        raise ValueError(f'Unknown checker options: {sorted(unknown_options)}')

    return argparse.Namespace(**{**DISABLED_OPTIONS, **overrides})


@pytest.fixture()
def run_validator_for_test_files() -> Callable[..., list[tuple]]:
    """Runs the checker against a file from `tests/test_files` with the given options."""
    def _run(filename: str, **config_options: object) -> list[tuple]:
        test_file_path = TEST_FILES_DIR / filename
        tree = ast.parse(test_file_path.read_text())

        FinePytestChecker.parse_options(build_options(**config_options))
        checker = FinePytestChecker(tree=tree, filename=str(test_file_path))

        return list(checker.run())

    return _run


@pytest.fixture()
def get_error_messages(run_validator_for_test_files) -> Callable[..., list[str]]:
    """Same as `run_validator_for_test_files`, but keeps only the error messages."""
    def _run(filename: str, **config_options: object) -> list[str]:
        return [error[2] for error in run_validator_for_test_files(filename, **config_options)]

    return _run

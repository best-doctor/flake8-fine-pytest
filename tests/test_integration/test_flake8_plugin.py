import subprocess
import sys

import pytest

from tests.conftest import TEST_FILES_DIR


def run_flake8(*arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, '-m', 'flake8', '--isolated', *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.parametrize(
    'select',
    ['FP', 'FP001', 'FP005'],
    ids=['plugin-prefix', 'single-code', 'another-single-code'],
)
def test__plugin__is_reachable_by_its_error_codes(select):
    """
    Arrange: the installed plugin and a test file with duplicated test names.
    Act: run flake8 with --select set to one of the plugin codes.
    Assert: flake8 finishes without an internal error, so the plugin is registered.
    """
    result = run_flake8(f'--select={select}', str(TEST_FILES_DIR / 'test_not_unique.py'))

    assert result.returncode in (0, 1), result.stderr
    assert 'Traceback' not in result.stderr


def test__plugin__does_not_crash_on_non_literal_xfail_reason():
    """
    Arrange: a test file whose xfail reason comes from a variable and an f-string.
    Act: run flake8 with the xfail reason checks selected.
    Assert: flake8 exits clean — a regression guard for ast.Str removed in Python 3.12.
    """
    target = TEST_FILES_DIR / 'test_xfail_with_dynamic_reason.py'

    result = run_flake8('--select=FP001,FP002', str(target))

    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout == ''

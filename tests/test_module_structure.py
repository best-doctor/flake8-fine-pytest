import pytest


@pytest.mark.parametrize('allowed_directory, expected_errors', [
    [['test_unit'], 1],
    [['fixture_files'], 0],
    [None, 0],
])
def test_wrong_module_directory(allowed_directory, expected_errors, run_validator_for_test_files):
    errors = run_validator_for_test_files('test_modules_structures.py', allowed_directory)

    assert len(errors) == expected_errors

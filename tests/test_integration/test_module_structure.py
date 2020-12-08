import pytest


@pytest.mark.parametrize('allowed_directory, test_filepath, expected_errors', [
    [['test_unit'], 'test_modules_structures.py', 1],
    [['test_files'], 'test_nested_module_structure/test_nested_module.py', 0],
    [['test_files'], 'some_file.py', 0],
    [None, 'test_modules_structures.py', 0],
])
def test_wrong_module_directory(allowed_directory, test_filepath, expected_errors, run_validator_for_test_files):
    errors = run_validator_for_test_files(
        test_filepath,
        allowed_test_directories=allowed_directory,
    )

    assert len(errors) == expected_errors

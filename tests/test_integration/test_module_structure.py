import pytest


@pytest.mark.parametrize(
    ('allowed_test_directories', 'test_filepath', 'expected_errors_count'),
    [
        (['test_unit'], 'test_modules_structures.py', 1),
        (['test_files'], 'test_nested_module_structure/test_nested_module.py', 0),
        (['test_files'], 'some_file.py', 0),
        (None, 'test_modules_structures.py', 0),
    ],
    ids=['wrong-directory', 'nested-allowed-directory', 'not-a-test-file', 'watcher-disabled'],
)
def test__modules_structure_watcher__checks_test_file_location(
    allowed_test_directories, test_filepath, expected_errors_count, run_validator_for_test_files,
):
    """
    Arrange: a test file inside `test_files` and a list of allowed directories.
    Act: run the checker against that file.
    Assert: FP003 is reported only when the file sits outside the allowed directories.
    """
    errors = run_validator_for_test_files(
        test_filepath,
        allowed_test_directories=allowed_test_directories,
    )

    assert len(errors) == expected_errors_count


def test__modules_structure_watcher__error_message_lists_allowed_directories(get_error_messages):
    """
    Arrange: a test file that sits outside the allowed directories.
    Act: run the checker with two allowed directories configured.
    Assert: the FP003 message lists both allowed directories.
    """
    messages = get_error_messages(
        'test_modules_structures.py',
        allowed_test_directories=['test_unit', 'test_integration'],
    )

    assert len(messages) == 1
    assert messages[0].startswith('FP003 ')
    assert messages[0].endswith('Allowed directories: test_unit,test_integration')

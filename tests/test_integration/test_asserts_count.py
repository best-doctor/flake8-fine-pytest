import pytest


@pytest.mark.parametrize(
    ('test_filename', 'invalid_test_name'),
    [
        ('test_too_many_asserts.py', 'test_with_too_many_asserts'),
        ('test_async_too_many_asserts.py', 'test_async_with_too_many_asserts'),
    ],
    ids=['sync-test', 'async-test'],
)
def test__assert_count_watcher__reports_tests_over_the_limit(
    test_filename, invalid_test_name, get_error_messages,
):
    """
    Arrange: a file with a test holding more asserts than allowed.
    Act: run the checker with a limit of two asserts.
    Assert: FP005 is reported only for the test that went over the limit.
    """
    expected_message = (
        f'FP005 {invalid_test_name} has too many assert statements. '
        'Allowed count of asserts is 2'
    )

    messages = get_error_messages(test_filename, allowed_assert_count=2)

    assert messages == [expected_message]


def test__assert_count_watcher__is_silent_when_disabled(get_error_messages):
    """
    Arrange: a file with a test holding too many asserts.
    Act: run the checker with no assert limit configured.
    Assert: nothing is reported, the validator is disabled.
    """
    assert get_error_messages('test_too_many_asserts.py') == []

def test__signature_complexity_watcher__reports_too_many_arguments(get_error_messages):
    """
    Arrange: a file where a single test takes three fixtures and the rest take fewer.
    Act: run the checker with a limit of two arguments.
    Assert: FP004 is reported exactly for the test with the too complex signature.
    """
    expected_message = (
        'FP004 test_with_too_complex_signature has too complex signature. '
        'Allowed count of arguments is 2'
    )

    messages = get_error_messages(
        'test_complex_signature_tests.py',
        allowed_test_arguments_count=2,
    )

    assert messages == [expected_message]


def test__signature_complexity_watcher__is_silent_when_disabled(get_error_messages):
    """
    Arrange: a file with a test having a too complex signature.
    Act: run the checker with no argument limit configured.
    Assert: nothing is reported, the validator is disabled.
    """
    assert get_error_messages('test_complex_signature_tests.py') == []

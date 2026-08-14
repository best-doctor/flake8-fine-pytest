import pytest


@pytest.mark.parametrize(
    ('test_filename', 'expected_message'),
    [
        ('test_xfail_with_no_reason.py', 'FP002 xfailed test without reason'),
        ('test_xfail_with_empty_reason.py', 'FP001 xfailed test with empty reason'),
    ],
    ids=['no-reason-argument', 'empty-reason-argument'],
)
def test__xfail_watcher__reports_undocumented_marks(
    test_filename, expected_message, get_error_messages,
):
    """
    Arrange: a file with an xfail mark that has no reason or an empty one.
    Act: run the checker with the reason validator enabled.
    Assert: the matching FP001/FP002 error is reported.
    """
    messages = get_error_messages(test_filename, xfail_check_reason=True)

    assert messages == [expected_message]


def test__xfail_watcher__allows_reason_computed_at_runtime(get_error_messages):
    """
    Arrange: a file with xfail marks whose reason comes from a variable and an f-string.
    Act: run the checker with the reason validator enabled.
    Assert: nothing is reported, a non-literal reason counts as filled in and parsing survives.
    """
    assert get_error_messages('test_xfail_with_dynamic_reason.py', xfail_check_reason=True) == []


@pytest.mark.parametrize(
    'test_filename',
    ['test_xfail_with_no_reason.py', 'test_xfail_with_empty_reason.py'],
)
def test__xfail_watcher__is_silent_when_disabled(test_filename, get_error_messages):
    """
    Arrange: a file with a badly documented xfail mark.
    Act: run the checker with the reason validator disabled.
    Assert: nothing is reported, the validator is disabled.
    """
    assert get_error_messages(test_filename, xfail_check_reason=False) == []

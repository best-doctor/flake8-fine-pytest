import pytest


def test__unique_test_names_watcher__reports_every_duplicate(get_error_messages):
    """
    Arrange: a file with two pairs of same-named tests, one pair carrying a decorator.
    Act: run the checker with the unique names validator enabled.
    Assert: FP009 is reported for every repeated definition.
    """
    messages = get_error_messages('test_not_unique.py', force_unique_test_names=True)

    assert messages == [
        'FP009 Duplicate name test case (test_not_uniq)',
        'FP009 Duplicate name test case (test_not_uniq_with_decorator)',
    ]


def test__unique_test_names_watcher__reports_duplicated_async_tests(get_error_messages):
    """
    Arrange: a file with two same-named asynchronous tests.
    Act: run the checker with the unique names validator enabled.
    Assert: FP009 is reported for async def tests as well.
    """
    messages = get_error_messages('test_async_not_unique.py', force_unique_test_names=True)

    assert messages == ['FP009 Duplicate name test case (test_async_not_uniq)']


@pytest.mark.parametrize(
    'test_filename',
    ['test_not_unique.py', 'test_async_not_unique.py'],
)
def test__unique_test_names_watcher__is_silent_when_disabled(test_filename, get_error_messages):
    """
    Arrange: a file with same-named tests.
    Act: run the checker with the unique names validator disabled.
    Assert: nothing is reported, the validator is disabled.
    """
    assert get_error_messages(test_filename, force_unique_test_names=False) == []

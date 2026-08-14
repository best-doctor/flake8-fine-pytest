import pytest


@pytest.mark.parametrize(
    ('test_filename', 'invalid_test_name'),
    [
        ('test_with_fixtures.py', 'test_with_no_usefixtures_where_needed'),
        ('test_async_with_fixtures.py', 'test_async_with_no_usefixtures_where_needed'),
    ],
    ids=['sync-test', 'async-test'],
)
def test__usefixtures_watcher__reports_unreferenced_fixtures(
    test_filename, invalid_test_name, get_error_messages,
):
    """
    Arrange: a file with a test that takes fixtures but never references them in its body.
    Act: run the checker with the usefixtures validator enabled.
    Assert: FP010 is reported and lists only the unreferenced fixtures.
    """
    expected_message = (
        f'FP010 {invalid_test_name} should use '
        "fixtures as follows: @pytest.mark.usefixtures('caplog', 'tmp_path')"
    )

    messages = get_error_messages(test_filename, force_usefixtures=True)

    assert messages == [expected_message]


def test__usefixtures_watcher__ignores_test_class_methods_self_argument(get_error_messages):
    """
    Arrange: a file with a test class whose method only takes `self`.
    Act: run the checker with the usefixtures validator enabled.
    Assert: nothing is reported, `self` does not count as an unreferenced fixture.
    """
    assert get_error_messages('test_class_with_fixtures.py', force_usefixtures=True) == []


def test__usefixtures_watcher__handles_unusual_test_class_members(get_error_messages):
    """
    Arrange: a test class with an attribute, a helper, a method without self and a static one.
    Act: run the checker with the usefixtures validator enabled.
    Assert: FP010 is reported only for the static method, where self is not implied.
    """
    expected_message = (
        'FP010 test_static_method_with_unused_fixture should use '
        "fixtures as follows: @pytest.mark.usefixtures('caplog')"
    )

    messages = get_error_messages('test_class_edge_cases.py', force_usefixtures=True)

    assert messages == [expected_message]


def test__usefixtures_watcher__is_silent_when_disabled(get_error_messages):
    """
    Arrange: a file with a test that does not reference its declared fixtures.
    Act: run the checker with the usefixtures validator disabled.
    Assert: nothing is reported, the validator is disabled.
    """
    assert get_error_messages('test_with_fixtures.py', force_usefixtures=False) == []

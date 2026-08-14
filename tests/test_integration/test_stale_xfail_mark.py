import pytest


@pytest.mark.parametrize(
    ('test_filename', 'expected_lineno', 'expected_message'),
    [
        (
            'test_absent_xfail_until_mark.py',
            4,
            'FP006 xfail mark has wrong format. It should has `until` argument',
        ),
        (
            'test_xfail_until_wrong_format.py',
            4,
            'FP007 xfail mark has wrong format. '
            'It should has `until` argument with datetime.date type',
        ),
        (
            'test_stale_xfail.py',
            6,
            'FP008 stale xfail mark',
        ),
        (
            'test_stale_xfail_keyword_until.py',
            6,
            'FP008 stale xfail mark',
        ),
    ],
    ids=[
        'until-is-absent',
        'until-is-not-a-date',
        'until-is-in-the-past',
        'until-is-in-the-past-as-keywords',
    ],
)
def test__xfail_until_watcher__reports_wrong_until_argument(
    test_filename, expected_lineno, expected_message, run_validator_for_test_files,
):
    """
    Arrange: a file with an xfail mark missing `until`, holding a wrong one or a stale date.
    Act: run the checker with the `until` validator enabled.
    Assert: a single error with the expected message is reported on the mark's own line.
    """
    errors = run_validator_for_test_files(test_filename, xfail_check_until=True)

    assert len(errors) == 1
    assert errors[0][0] == expected_lineno
    assert errors[0][2] == expected_message


def test__xfail_until_watcher__handles_until_that_cannot_be_resolved_statically(
    get_error_messages,
):
    """
    Arrange: a file with an `until` computed at runtime and an `until` built from an impossible date.
    Act: run the checker with the `until` validator enabled.
    Assert: the checker survives; only a statically resolvable date can be judged stale.
    """
    messages = get_error_messages('test_xfail_until_not_a_literal.py', xfail_check_until=True)

    assert messages == [
        'FP007 xfail mark has wrong format. It should has `until` argument with datetime.date type',
    ]


@pytest.mark.parametrize(
    'test_filename',
    [
        'test_absent_xfail_until_mark.py',
        'test_xfail_until_wrong_format.py',
        'test_stale_xfail.py',
    ],
)
def test__xfail_until_watcher__is_silent_when_disabled(test_filename, get_error_messages):
    """
    Arrange: a file with a badly formatted `until` argument.
    Act: run the checker with the `until` validator disabled.
    Assert: nothing is reported, the validator is disabled.
    """
    assert get_error_messages(test_filename, xfail_check_until=False) == []

import pytest


@pytest.mark.parametrize(
    'enable_validator, expected_errors_count',
    [
        (True, 1),
        (False, 0),
    ],
)
def test_xfail_with_no_reason(
    enable_validator, expected_errors_count,
    run_validator_for_test_files,
):
    errors = run_validator_for_test_files(
        'test_xfail_with_no_reason.py',
        xfail_check_reason=enable_validator,
    )

    assert len(errors) == expected_errors_count


@pytest.mark.parametrize(
    'enable_validator, expected_errors_count',
    [
        (True, 1),
        (False, 0),
    ],
)
def test_xfail_with_empty_reason(
    enable_validator, expected_errors_count,
    run_validator_for_test_files,
):
    errors = run_validator_for_test_files(
        'test_xfail_with_empty_reason.py',
        xfail_check_reason=enable_validator,
    )

    assert len(errors) == expected_errors_count

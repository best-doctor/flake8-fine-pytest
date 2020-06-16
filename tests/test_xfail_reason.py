def test_xfail_with_no_reason(run_validator_for_test_files):
    errors = run_validator_for_test_files('xfailed_test_with_no_reason.py')

    assert len(errors) == 1


def test_xfail_with_empty_reason(run_validator_for_test_files):
    errors = run_validator_for_test_files('xfailed_test_with_empty_reason.py')

    assert len(errors) == 1

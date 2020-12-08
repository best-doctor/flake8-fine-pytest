def test_unique_names(run_validator_for_test_files):
    errors = run_validator_for_test_files(
        'test_not_unique.py',
        force_unique_test_names=True,
    )

    assert len(errors) == 2
    assert errors[0][2] == 'FP009 Duplicate name test case (test_not_uniq)'
    assert errors[1][2] == 'FP009 Duplicate name test case (test_not_uniq_with_decorator)'

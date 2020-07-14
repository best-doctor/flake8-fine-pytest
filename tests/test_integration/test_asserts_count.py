def test_signature_complexity(run_validator_for_test_files):
    errors = run_validator_for_test_files('test_too_many_asserts.py', allowed_assert_count=2)
    expected_error_message = (
        'FP005 test_with_too_many_asserts has too many assert statements. Allowed count of asserts is 2'
    )

    assert len(errors) == 1
    assert errors[0][2] == expected_error_message

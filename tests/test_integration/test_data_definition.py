def test_too_long_data_definitions(run_validator_for_test_files):
    errors = run_validator_for_test_files('too_long_data_definition.py')

    assert len(errors) == 1
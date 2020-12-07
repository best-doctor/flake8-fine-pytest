def test_fixtures_should_be_in_usefixtures(run_validator_for_test_files):
    expected_error_message = (
        'FP009 test_with_no_usefixtures_where_needed should use '
        "fixtures as follows: @pytest.mark.usefixtures('caplog', 'tmp_path')"
    )

    errors = run_validator_for_test_files(
        'test_with_fixtures.py',
        force_usefixtures=True,
    )

    assert len(errors) == 1
    assert errors[0][2] == expected_error_message


def test_testclass_ignored(run_validator_for_test_files):
    errors = run_validator_for_test_files(
        'test_class_with_fixtures.py',
        force_usefixtures=True,
    )

    assert not errors


def test_fixtures_should_be_in_usefixtures_but_validator_is_disabled(
    run_validator_for_test_files,
):
    errors = run_validator_for_test_files(
        'test_with_fixtures.py',
        force_usefixtures=False,
    )

    assert not errors

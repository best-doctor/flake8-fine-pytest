import pytest

REASON = 'flaky on CI'


@pytest.mark.xfail(reason=REASON)
def test_xfail_with_reason_from_variable() -> None:
    pass


@pytest.mark.xfail(reason=f'{REASON} for now')
def test_xfail_with_reason_from_fstring() -> None:
    pass

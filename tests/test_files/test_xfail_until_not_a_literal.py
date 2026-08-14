import pytest

from datetime import date, timedelta


@pytest.mark.xfail(reason='Test', until=date.today() + timedelta(days=1))
def test_xfail_until_computed_at_runtime():
    pass


@pytest.mark.xfail(reason='Test', until=date(2020, 13, 40))
def test_xfail_until_impossible_date():
    pass


@pytest.mark.skip
@pytest.mark.xfail(reason='Test', until=date(2999, 1, 1))
def test_xfail_alongside_other_decorators():
    pass

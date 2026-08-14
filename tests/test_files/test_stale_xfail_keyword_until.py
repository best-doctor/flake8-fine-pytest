import pytest

from datetime import date


@pytest.mark.xfail(reason='Test', until=date(year=1900, month=9, day=7))
def test_stale_xfail_with_keyword_until():
    pass

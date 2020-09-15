import pytest

from datetime import date


@pytest.mark.xfail(reason='Test', until=date(1900, 9, 7))
def test_stale_xfail_until_mark_two():
    pass

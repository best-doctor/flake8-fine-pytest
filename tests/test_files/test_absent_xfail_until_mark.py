import pytest


@pytest.mark.xfail(reason='Test')
def test_stale_xfail_until_mark_one():
    pass

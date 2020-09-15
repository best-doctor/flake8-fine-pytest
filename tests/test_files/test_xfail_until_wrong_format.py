import pytest


@pytest.mark.xfail(reason='Test', until='wrong format')
def test_xfail_mark_until_wrong_format():
    pass

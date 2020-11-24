import pytest


def test_with_no_usefixtures_where_needed(caplog, capsys, tmp_path):
    assert capsys


@pytest.mark.usefixtures('caplog', 'tmp_path')
def test_with_usefixtures_where_needed(capsys):
    assert capsys

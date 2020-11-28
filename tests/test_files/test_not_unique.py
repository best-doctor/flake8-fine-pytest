import pytest


def test_not_uniq():
    pass


def test_not_uniq():
    pass


@pytest.mark.parametrize('test', ('test',))
def test_not_uniq_with_decorator(test):
    pass


@pytest.mark.parametrize('test', ('test2',))
def test_not_uniq_with_decorator(test):
    pass

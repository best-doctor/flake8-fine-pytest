import pytest


def test_not_uniq() -> None:
    pass


def test_not_uniq() -> None:
    pass


@pytest.mark.parametrize('test', ('test',))
def test_not_uniq_with_decorator(test) -> None:
    pass


@pytest.mark.parametrize('test', ('test2',))
def test_not_uniq_with_decorator(test) -> None:
    pass

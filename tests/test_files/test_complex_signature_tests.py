import pytest


@pytest.fixture
def one(a=1, b=2, c=3, d=4):
    pass


@pytest.fixture
def two():
    pass


@pytest.fixture
def three():
    pass


def test_with_too_complex_signature(one, two, three):
    assert (2 + 2) == 4


def test_with_normal_signature(one):
    assert (2 + 2) == 4


def test_with_empty_signature():
    assert (2 + 2) == 4 

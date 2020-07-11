import pytest


@pytest.fixture
def one():
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

def test_with_too_many_asserts():
    assert 1 + 1 == 2
    assert 2 + 2 == 4
    assert 3 + 3 == 6
    assert 4 + 4 == 8


def test_with_fine_asserts():
    assert 1 + 1 == 2


def usual_function_with_too_many_asserts():
    assert 1 + 1 == 2
    assert 2 + 2 == 4
    assert 3 + 3 == 6
    assert 4 + 4 == 8

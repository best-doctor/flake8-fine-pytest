async def test_async_with_too_many_asserts():
    assert 1 + 1 == 2
    assert 2 + 2 == 4
    assert 3 + 3 == 6


async def test_async_with_fine_asserts():
    assert 1 + 1 == 2

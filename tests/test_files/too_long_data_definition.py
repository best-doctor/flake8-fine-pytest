def test_too_long_data_definitio():
    test_data = [
        {'user_id': 1, 'is_banned': False, 'is_staff': True},
        {'user_id': 2, 'is_banned': False, 'is_staff': False},
        {'user_id': 3, 'is_banned': True, 'is_staff': False},
        {'user_id': 4, 'is_banned': False, 'is_staff': True},
        {'user_id': 5, 'is_banned': True, 'is_staff': True},
        {'user_id': 6, 'is_banned': True, 'is_staff': True},
    ]
import ast

import pytest

from flake8_fine_pytest.watchers.usefixtures import is_static_method


@pytest.mark.parametrize(
    ('source', 'expected_result'),
    [
        ('@staticmethod\ndef test_one(): pass', True),
        ('@classmethod\ndef test_one(cls): pass', False),
        ('@pytest.mark.skip\ndef test_one(self): pass', False),
        ('def test_one(self): pass', False),
    ],
    ids=['staticmethod', 'classmethod', 'unrelated-decorator', 'no-decorators'],
)
def test__is_static_method__detects_staticmethod_decorator(source, expected_result):
    """
    Arrange: a test class method definition, with or without a decorator.
    Act: check whether the method is a static one.
    Assert: True only for the method wrapped in @staticmethod.
    """
    node = ast.parse(source).body[0]

    assert is_static_method(node) is expected_result

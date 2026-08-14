import pathlib

import pytest

from flake8_fine_pytest.utils import get_stem


@pytest.mark.parametrize(
    ('filepath', 'expected_stem'),
    [
        ('tests/test_unit/test_utils.py', 'test_utils'),
        ('test_utils.py', 'test_utils'),
        ('tests/test_unit', 'test_unit'),
        (pathlib.Path('tests/test_unit/test_utils.py'), 'test_utils'),
    ],
    ids=['nested-file', 'bare-file', 'directory', 'path-object'],
)
def test__get_stem__returns_name_without_suffix(filepath, expected_stem):
    """
    Arrange: a path to a file or a directory, given as a string or as a Path.
    Act: take the stem of that path.
    Assert: the name comes back without its suffix and without parent directories.
    """
    assert get_stem(filepath) == expected_stem

import pytest

from flake8_fine_pytest.watchers.modules_structure import get_file_directory


@pytest.mark.parametrize(
    ('filepath', 'expected_directory'),
    [
        ('project/tests/test_unit/test_foo.py', 'test_unit'),
        ('project/tests/test_unit/test_foo/test_bar.py', 'test_unit'),
        ('project/tests/test_unit/test_foo/test_bar/test_baz.py', 'test_unit'),
        ('project/tests/helpers/test_foo.py', 'helpers'),
    ],
    ids=['flat-layout', 'one-nesting-level', 'two-nesting-levels', 'non-test-directory'],
)
def test__get_file_directory__climbs_up_to_the_top_test_package(filepath, expected_directory):
    """
    Arrange: a path to a test module, possibly nested inside test_ packages.
    Act: resolve the top-most test directory for that file.
    Assert: the name of the outermost directory not starting with `test_` comes back.
    """
    assert get_file_directory(filepath) == expected_directory

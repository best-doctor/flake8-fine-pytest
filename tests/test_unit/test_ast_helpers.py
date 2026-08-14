import ast
import textwrap

import pytest

from flake8_fine_pytest.ast_helpers import get_wrong_xfail_decorator_lines


@pytest.mark.parametrize(
    ('source', 'expected_empty_reason', 'expected_absent_reason'),
    [
        ('@pytest.mark.xfail\ndef test_one(): pass', set(), {1}),
        ('@pytest.mark.xfail()\ndef test_one(): pass', set(), {1}),
        ("@pytest.mark.xfail(reason='')\ndef test_one(): pass", {1}, set()),
        ('@pytest.mark.xfail(reason=None)\ndef test_one(): pass', {1}, set()),
        ("@pytest.mark.xfail(reason='flaky')\ndef test_one(): pass", set(), set()),
        ('@pytest.mark.xfail(reason=REASON)\ndef test_one(): pass', set(), set()),
        ("@pytest.mark.xfail(reason=f'{REASON}')\ndef test_one(): pass", set(), set()),
        ("@pytest.mark.xfail(strict=True, reason='flaky')\ndef test_one(): pass", set(), set()),
        ('@pytest.mark.xfail(strict=True)\ndef test_one(): pass', set(), {1}),
        ('@pytest.mark.skip\ndef test_one(): pass', set(), set()),
    ],
    ids=[
        'bare-mark',
        'called-without-arguments',
        'empty-string-reason',
        'none-reason',
        'filled-reason',
        'reason-from-variable',
        'reason-from-fstring',
        'reason-after-another-keyword',
        'other-keyword-without-reason',
        'unrelated-mark',
    ],
)
def test__get_wrong_xfail_decorator_lines__classifies_marks(
    source, expected_empty_reason, expected_absent_reason,
):
    """
    Arrange: a source snippet with a single pytest mark on its first line.
    Act: parse the tree and collect the lines of badly documented xfail marks.
    Assert: the mark lands in the empty-reason or the absent-reason set as expected.
    """
    tree = ast.parse(textwrap.dedent(source))

    empty_reason, absent_reason = get_wrong_xfail_decorator_lines(tree)

    assert empty_reason == expected_empty_reason
    assert absent_reason == expected_absent_reason


def test__get_wrong_xfail_decorator_lines__reports_every_mark_in_a_module():
    """
    Arrange: a module carrying three xfail marks of differing quality.
    Act: parse the tree and collect the lines of badly documented marks.
    Assert: each problematic mark lands in its own set with its own line number.
    """
    source = textwrap.dedent(
        """
        @pytest.mark.xfail
        def test_one(): pass

        @pytest.mark.xfail(reason='')
        def test_two(): pass

        @pytest.mark.xfail(reason='documented')
        def test_three(): pass
        """,
    )
    tree = ast.parse(source)

    empty_reason, absent_reason = get_wrong_xfail_decorator_lines(tree)

    assert empty_reason == {5}
    assert absent_reason == {2}

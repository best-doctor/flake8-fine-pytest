import ast
from datetime import date

import pytest

from flake8_fine_pytest.watchers.xfail_until_argument_watcher import parse_date_call


@pytest.mark.parametrize(
    ('source', 'expected_date'),
    [
        ('date(2030, 9, 7)', date(2030, 9, 7)),
        ('datetime.date(1900, 1, 31)', date(1900, 1, 31)),
        ('date(year=2030, month=9, day=7)', date(2030, 9, 7)),
        ('date(2030, month=9, day=7)', date(2030, 9, 7)),
        ('date(2030, 9, day=7)', date(2030, 9, 7)),
        ('date(2020, 13, 40)', None),
        ('date(2030, 9)', None),
        ('date(2030, 9, 7, 12)', None),
        ('date(year=2030, month=9)', None),
        ('date(2030, 9, dya=7)', None),
        ('date(year, 9, 7)', None),
        ("date('2030', 9, 7)", None),
        ('date.today()', None),
        ('SOME_DATE', None),
    ],
    ids=[
        'plain-date-call',
        'qualified-date-call',
        'all-keyword-arguments',
        'one-positional-two-keyword',
        'two-positional-one-keyword',
        'impossible-calendar-date',
        'too-few-arguments',
        'too-many-arguments',
        'missing-keyword-argument',
        'misspelled-keyword-argument',
        'argument-is-a-name',
        'argument-is-a-string',
        'no-arguments',
        'not-a-call',
    ],
)
def test__parse_date_call__resolves_only_literal_dates(source, expected_date):
    """
    Arrange: the expression used as the `until` argument of an xfail mark.
    Act: try to resolve it into a date statically.
    Assert: a date comes back only for a valid literal call, otherwise None.
    """
    node = ast.parse(source, mode='eval').body

    assert parse_date_call(node) == expected_date

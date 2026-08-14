# flake8-fine-pytest

[![Build Status](https://github.com/best-doctor/flake8-fine-pytest/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/best-doctor/flake8-fine-pytest/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/flake8-fine-pytest.svg)](https://badge.fury.io/py/flake8-fine-pytest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-fine-pytest)

An extension for flake8 that validates tests structure, extra style and readability.

## Installation

```terminal
pip install flake8-fine-pytest
```

Requires Python 3.10+ and flake8 5+.
See the [changelog](CHANGELOG.md) for release notes and upgrade notes.

## Error codes

| Code | Description |
| --- | --- |
| FP001 | xfailed test with empty reason |
| FP002 | xfailed test without reason |
| FP003 | test module is in the wrong directory |
| FP004 | test has too complex signature |
| FP005 | test has too many assert statements |
| FP006 | xfail mark has no `until` argument |
| FP007 | xfail `until` argument is not a `datetime.date` |
| FP008 | stale xfail mark |
| FP009 | duplicate test case name |
| FP010 | fixtures should be moved to `pytest.mark.usefixtures` |

## Configuration

Options can be set in any file flake8 reads. With
[Flake8-pyproject](https://pypi.org/project/Flake8-pyproject/) installed they live in
`pyproject.toml`:

```toml
[tool.flake8]
allowed_test_directories = ["test_unit", "test_integration", "test_api"]
allowed_test_arguments_count = 6
allowed_assert_count = 6
xfail_check_until = true
xfail_check_reason = true
force_unique_test_names = true
force_usefixtures = true
```

The same options in `setup.cfg`:

```cfg
[flake8]
allowed_test_directories = test_unit,test_integration,test_api
allowed_test_arguments_count = 6
```

Every validator is enabled by default.

## Checks

### Reason in the xfail mark (FP001, FP002)

Validates that an xfail mark explains itself:

```python
@pytest.mark.xfail(reason='Super annoying test, fix it later')
```

It helps everyone easily understand what was the problem in the first place
and reduces amount of time wasted on fixing xfailed tests.

A reason built at runtime — from a variable or an f-string — is accepted as filled in,
since its value cannot be known statically.

### Test modules location (FP003)

Validates that test modules are in the described directories. If a file with prefix
`test_` is not in the allowed directories list, it will raise an error:

```shell
tests/test_models.py:0:1: FP003 File tests/test_models.py is in the wrong directory.
Allowed directories: test_unit,test_integration,test_api,test_migration
```

### Signature complexity (FP004)

Validates that a test function has a not too complicated signature:

```shell
tests/test_integration/test_models.py:64:1: FP004 test_save_method has too complex
signature. Allowed count of arguments is 6
```

### Assertion block complexity (FP005)

Validates that a test function has a not too complicated assertion block:

```shell
tests/test_integration/test_models.py:64:1: FP005 test_save_method has
too many assert statements. Allowed count of asserts is 6
```

### The `until` argument of the xfail mark (FP006, FP007, FP008)

The `until` argument must be specified as a valid `datetime.date` value
and not older than the current date. For example:

```python
@pytest.mark.xfail(reason='Test', until=date(2020, 9, 7))
```

If the `until` argument is missing:

```shell
tests/test_unit/test_utils.py:128:1: FP006 xfail mark has wrong format.
It should has `until` argument
```

If it is specified in a wrong format:

```shell
tests/test_unit/test_utils.py:128:1: FP007 xfail mark has wrong format.
It should has `until` argument with datetime.date type
```

If the mark is too old:

```shell
tests/test_unit/test_utils.py:128:1: FP008 stale xfail mark
```

A date that cannot be resolved statically, such as `date.today() + timedelta(days=7)`,
is never reported as stale.

### Unique test names (FP009)

Validates that test functions within a module use unique names, so that no test case
is silently shadowed by a later definition.

### Fixtures in usefixtures (FP010)

Validates that a test function uses `pytest.mark.usefixtures`
for those fixtures, which are not directly referenced in test body.

For example, checking this function:

```python
# file: test_something.py
def test_something(fixture_one, fixture_two):
    assert fixture_two.some_attribute is not None
```

would raise:

```shell
tests/test_unit/test_something.py:2:0: FP010 test_something should use fixtures
as follows: @pytest.mark.usefixtures('fixture_one')
```

## Example

Sample file:

```python
# test.py

@pytest.mark.xfail(reason='')
def test_xfail() -> None:
    pass

@pytest.mark.xfail
def test_xfail_without_reason() -> None:
    pass
```

Usage:

```terminal
$ flake8 test.py
test.py:1:1: FP001 xfailed test with empty reason
test.py:5:1: FP002 xfailed test without reason
```

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- The project is managed with [uv](https://docs.astral.sh/uv/).
  Run `make install` to set up the environment and the pre-commit hooks.
- You can run all checks and tests with `make check`.
  Please do it before CI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.

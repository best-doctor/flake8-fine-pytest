# flake8-fine-pytest

[![Build Status](https://github.com/best-doctor/flake8-fine-pytest/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/best-doctor/flake8-fine-pytest/actions/workflows/build.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/ea5c318a4508b00d7be2/maintainability)](https://codeclimate.com/github/best-doctor/flake8-fine-pytest/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ea5c318a4508b00d7be2/test_coverage)](https://codeclimate.com/github/best-doctor/flake8-fine-pytest/test_coverage)
[![PyPI version](https://badge.fury.io/py/flake8-fine-pytest.svg)](https://badge.fury.io/py/flake8-fine-pytest)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-fine-pytest)

An extension for flake8 that validates tests structure, extra style and readability.

Right now our checker:
1) validates existence of reason in

```python
@pytest.mark.xfail(reason='Super annoying test, fix it later')
```

It helps everyone easily understand what was the problem in the first place
and reduces amount of time wasted on fixing xfailed tests.

2) validates that test modules are in the described directories. It can be configured
in `setup.cfg` file:

  ```cfg
  allowed_test_directories = test_unit,test_integration,test_api
  ```

If file with prefix `test_` is not in allowed directories list, it will raise
an error:

```shell
tests/test_models.py:0:1: FP003 File tests/test_models.py is in the wrong directory.
Allowed directories: test_unit,test_integration,test_api,test_migration
```

3) validates that test function has a not too complicated signature. Allowed number
of arguments for test can be configured in `setup.cfg` file:

  ```cfg
  allowed_test_arguments_count = 6
  ```

If test function has too complex signature, it will raise an error:

```shell
tests/test_integration/test_models.py:64:1: FP004 test_save_method has too complex
signature. Allowed count of arguments is 6
```

4) validates that test function has a not too complicated assertion block.
Allowed number of asserts for test can be configured in `setup.cfg` file:

  ```cfg
  allowed_assert_count = 6
  ```

If test function has too complex assertion block, it will raise an error:

```shell
tests/test_integration/test_models.py:64:1: FP005 test_save_method has
too many assert statements. Allowed count of asserts is 6
```

5) validates that `xfail` decorator has until argument.
Until argument must be specified as a valid `datetime.date` value
and not older than the current date. For example:

`@pytest.mark.xfail(reason='Test', until=date(2020, 9, 7))`

If `xfail` does not have such mark, flake8 will raise an error:

```shell
tests/test_unit/test_utils.py:128:1: FP006 xfail mark has wrong format.
It should has `until` argument
```

in case you forgot to specify `until` argument

```shell
tests/test_unit/test_utils.py:128:1: FP007 xfail mark has wrong format.
It should has `until` argument with datetime.date type
```

in case you specified it in wrong format

```shell
tests/test_unit/test_utils.py:128:1: FP008 stale xfail mark
```

in case you have too old `xfail` mark

6) validates that test function uses unique names

7) validates that test function uses `pytest.mark.usefixtures`
for those fixtures, which are not directly referenced in test body

For example, checking this function

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

## Installation

```terminal
pip install flake8-fine-pytest
```

## Example

Sample file:

```python
# test.py

@pytest.mark.xfail(reason='')
def test_xfail() -> None:
    pass

@pytest.mark.xfail
def test_xfail() -> None:
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

- You can run all checks and tests with `make check`.
  Please do it before CI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.

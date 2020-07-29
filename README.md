# flake8-fine-pytest

[![Build Status](https://travis-ci.org/best-doctor/flake8-fine-pytest.svg?branch=master)](https://travis-ci.org/best-doctor/flake8-fine-pytest)
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
  allowed_test_directories= test_unit,test_integration,test_api
  ```

If file with prefix `test_` is not in allowed directories list, it will raise
an error:

```shell
tests/test_models.py:0:1: FP003 File tests/test_models.py is in the wrong directory.
Allowed directories: test_unit,test_integration,test_api,test_migration
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
## Code prerequisites

1. Python 3.8+;

## Code prerequisites

1. Python 3.8+.

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`.
  Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.

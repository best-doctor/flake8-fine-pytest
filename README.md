# flake8-fine-pytest

An extension for flake8 that validates tests structure, extra style and readability.

Right now our checker:
    1) validates existence of reason in

```python
    @pytest.mark.xfail(reason='Super annoying test, fix it later')
```

It helps everyone easily understand what was the problem in the first place
and reduces amount of time wasted on fixing xfailed tests.

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
  Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/python_styleguide.md).
  Sorry, styleguide is available only in Russian for now.
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.
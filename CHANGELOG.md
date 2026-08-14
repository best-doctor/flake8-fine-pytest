# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-08-14

### Removed

- **Breaking:** dropped support for Python 3.7, 3.8 and 3.9. The minimum supported
  version is now Python 3.10.
- Dropped the CodeClimate integration along with `.codeclimate.yml`.
- Dropped `setup.py`, `setup.cfg`, `requirements_dev.txt`, `.flake_master`
  and the `mdl` configuration (`.mdlrc`, `.mdlrc.rb`).

### Added

- Support for Python 3.11, 3.12, 3.13 and 3.14.
- All checks now recognise `async def` tests. Previously every watcher matched only
  `ast.FunctionDef`, so asynchronous tests silently bypassed all ten checks.
- `pyproject.toml` as the single source of packaging, lint, type-check, test and
  coverage configuration. Plugin options can now be set under `[tool.flake8]` via
  [Flake8-pyproject](https://pypi.org/project/Flake8-pyproject/).
- A `.pre-commit-config.yaml` running flake8, mypy, pytest, `uv lock` and markdownlint.
- A unit test suite under `tests/test_unit`, alongside the existing integration tests,
  and an end-to-end test that runs the plugin through the real flake8 CLI.
- This changelog.

### Fixed

- **Crash on Python 3.12+**: the xfail reason parser referenced `ast.Str`, removed in
  Python 3.12, and raised `AttributeError` inside flake8 whenever a `reason` was not a
  plain literal, e.g. `@pytest.mark.xfail(reason=SOME_CONSTANT)`.
- **Crash on malformed `until` dates**: `@pytest.mark.xfail(until=date(2020, 13, 40))`
  raised an uncaught `ValueError`, as did any `date()` call without exactly three
  literal arguments. Such marks are now left unreported rather than aborting the run.
- **FP008 false negative**: a stale mark written with keyword arguments, such as
  `until=date(year=2020, month=1, day=1)`, was never reported. Both the positional
  and the keyword form are now understood.
- **FP001 false positive**: a `reason` built from a variable or an f-string was reported
  as an empty reason. A non-literal reason is now treated as filled in, since its value
  cannot be known statically.
- **Plugin registration**: the entry point was registered as `FP001`, so selecting a
  single other code, such as `--select=FP005`, would not load the plugin at all. It is
  now registered under the `FP` prefix.
- Compatibility with flake8 5+, whose `OptionManager` signature changed.

### Changed

- Publishing now uses PyPI trusted publishing instead of a stored username/password.
- Replaced `safety` with `pip-audit` for dependency auditing.
- Replaced the Ruby `mdl` markdown linter with `markdownlint-cli2`.
- Merged the duplicated `build.yml` and `build_pr.yml` workflows into a single
  `ci.yml`, and switched dependency installation to [uv](https://docs.astral.sh/uv/).
- Test coverage is now enforced at 100% with branch coverage enabled.
- Dropped the unmaintained `flake8-expression-complexity` and `flake8-functions` from
  the development dependencies; both break flake8 on Python 3.12+ for the same
  `ast.Str` reason, and neither has a fixed release.

## [1.0.3] - 2022-02-24

### Added

- Support for Python 3.10.

## [1.0.2] - 2021-01-14

### Added

- Support for Python 3.9.

## [1.0.0] - 2020-12-22

### Changed

- The xfail validators are enabled by default.

## [0.1.0] - 2020-09-15

### Added

- FP006, FP007 and FP008: validation of the `until` argument of the xfail mark.

## [0.0.3] - 2020-07-14

### Added

- FP004 and FP005: test signature and assertion count validation.

## [0.0.2] - 2020-06-30

### Added

- FP003: test modules structure validation.

## [0.0.1] - 2020-05-11

### Added

- Initial release with FP001 and FP002: xfail reason validation.

[2.0.0]: https://github.com/best-doctor/flake8-fine-pytest/compare/v1.0.3...v2.0.0
[1.0.3]: https://github.com/best-doctor/flake8-fine-pytest/releases/tag/v1.0.3

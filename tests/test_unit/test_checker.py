import ast

import pytest
from flake8.options.manager import OptionManager

from flake8_fine_pytest import __version__
from flake8_fine_pytest.checker import FinePytestChecker
from flake8_fine_pytest.watchers.base import BaseWatcher

EXPECTED_OPTIONS = (
    '--allowed-test-directories',
    '--allowed-test-arguments-count',
    '--allowed-assert-count',
    '--xfail-check-until',
    '--xfail-check-reason',
    '--force-unique-test-names',
    '--force-usefixtures',
)


@pytest.fixture()
def option_manager() -> OptionManager:
    return OptionManager(
        version=__version__,
        plugin_versions='',
        parents=[],
        formatter_names=[],
    )


def test__add_options__registers_every_checker_option(option_manager):
    """
    Arrange: a fresh flake8 OptionManager.
    Act: register the checker options on it.
    Assert: every plugin option is registered and readable from a config file.
    """
    FinePytestChecker.add_options(option_manager)

    registered_options = {option.long_option_name for option in option_manager.options}
    assert registered_options == set(EXPECTED_OPTIONS)
    assert all(option.parse_from_config for option in option_manager.options)


@pytest.mark.parametrize(
    ('option_name', 'expected_default'),
    [
        ('--allowed-test-directories', ['test_unit', 'test_integration']),
        ('--allowed-test-arguments-count', 6),
        ('--allowed-assert-count', 6),
        ('--xfail-check-until', True),
        ('--xfail-check-reason', True),
        ('--force-unique-test-names', True),
        ('--force-usefixtures', True),
    ],
)
def test__add_options__defaults_keep_all_validators_enabled(
    option_name, expected_default, option_manager,
):
    """
    Arrange: a fresh flake8 OptionManager.
    Act: register the checker options and collect their default values.
    Assert: the default enables the validator, so the plugin works unconfigured.
    """
    FinePytestChecker.add_options(option_manager)

    defaults = {option.long_option_name: option.default for option in option_manager.options}

    assert defaults[option_name] == expected_default


def test__checker__reports_the_plugin_metadata():
    """
    Arrange: the checker class as flake8 sees it.
    Act: read the plugin metadata off it.
    Assert: the name and the version match the package metadata.
    """
    assert FinePytestChecker.name == 'flake8-fine-pytest'
    assert FinePytestChecker.version == __version__


def test__base_watcher_run__is_not_implemented():
    """
    Arrange: the base watcher, with no run implementation of its own.
    Act: try to run it directly.
    Assert: NotImplementedError is raised, subclasses must define the check themselves.
    """
    watcher = BaseWatcher(options=None, filename='test_foo.py', tree=ast.parse(''))

    with pytest.raises(NotImplementedError):
        watcher.run()

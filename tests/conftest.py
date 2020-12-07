import os
import ast

import pytest
from flake8.options.manager import OptionManager

from flake8_fine_pytest.checker import FinePytestChecker


def parse_options(**config):
    options = OptionManager()

    options.allowed_test_directories = config.get('allowed_test_directories', None)
    options.allowed_test_arguments_count = config.get('allowed_test_arguments_count', None)
    options.allowed_assert_count = config.get('allowed_assert_count', None)
    options.xfail_check_until = config.get('xfail_check_until', False)
    options.xfail_check_reason = config.get('xfail_check_reason', False)
    options.force_usefixtures = config.get('force_usefixtures', False)

    FinePytestChecker.parse_options(options)


@pytest.fixture
def run_validator_for_test_files():
    def _run(filename, **config_options):
        test_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'test_files',
            filename,
        )

        with open(test_file_path, 'r') as file_handler:
            raw_content = file_handler.read()

        tree = ast.parse(raw_content)
        checker = FinePytestChecker(tree=tree, filename=test_file_path)

        parse_options(**config_options)

        return list(checker.run())

    return _run

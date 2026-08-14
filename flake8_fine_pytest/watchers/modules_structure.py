import pathlib

from flake8_fine_pytest.utils import get_stem
from flake8_fine_pytest.watchers.base import BaseWatcher


def get_file_directory(filepath: str) -> str:
    directory = pathlib.Path(filepath).parent

    while directory.parent.stem.startswith('test_'):
        directory = directory.parent

    return get_stem(directory)


class ModulesStructureWatcher(BaseWatcher):
    config_option = 'allowed_test_directories'
    error_template = (
        'FP003 File {filepath} is in the wrong directory. Allowed directories: {allowed_directories}'
    )

    def run(self) -> None:
        allowed_test_directories = self.options.allowed_test_directories

        if get_file_directory(self.filename) in allowed_test_directories:
            return

        error_message = self.error_template.format(
            filepath=self.filename,
            allowed_directories=','.join(allowed_test_directories),
        )
        self.add_error((0, 0, error_message))

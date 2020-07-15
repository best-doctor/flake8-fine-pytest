import ast
from typing import List, Optional, Union

from flake8_fine_pytest.watchers.base import BaseWatcher

class LongDataDefinitionWathcer(BaseWatcher):
    error_template = (
                      'FP004 Test {test_name} has data definition longer than {numbers_of_line}. '
        )
    def run(self) -> None:
        for node in ast.walk(self.tree):
             if isinstance(node, ast.Name):
                 print(node.name)
        
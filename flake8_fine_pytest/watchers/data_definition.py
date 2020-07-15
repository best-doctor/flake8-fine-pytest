import ast

from flake8_fine_pytest.watchers.base import BaseWatcher


class LongDataDefinitionWathcer(BaseWatcher):
    error_template = (
        'FP004 Test {filename} has data definition longer than {max_data_lenght} strings.'
    )

    def run(self) -> None:
        max_data_lenght = self.options.max_number_line_data_definition
        longdata = 0
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Assign):
                longdata += node.end_lineno - node.lineno
        if longdata > max_data_lenght:
            self.add_error((0,
                            0,
                            self.error_template.format(filename=self.filename, max_data_lenght=max_data_lenght)))

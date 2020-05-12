import ast
import typing


def get_xfail_line_numbers(ast_tree: ast.AST) -> typing.Set[int]:
    xfail_without_reason: typing.Set[int] = set()
    for decorator in ast.walk(ast_tree):
        if isinstance(decorator, (ast.Attribute)) and decorator.attr == 'xfail':
            xfail_without_reason.add(decorator.lineno)
    return xfail_without_reason


def get_xfail_reason_value(node: ast.AST, xfail_lines: typing.Set[int]) -> str:
    if isinstance(node, ast.Call) and node.lineno in xfail_lines:
        for keyword in node.keywords:
            if keyword.arg == 'reason':
                return keyword.value.value  # type: ignore
    return 'Wrong ast instance'


def get_xfail_reasons(ast_tree: ast.AST) -> typing.Dict:
    xfail_lines = get_xfail_line_numbers(ast_tree)
    xfail_reasons: typing.Dict = {}
    for node in ast.walk(ast_tree):
        reason_value = get_xfail_reason_value(node, xfail_lines)
        if reason_value != 'Wrong ast instance':
            xfail_reasons[node.lineno] = get_xfail_reason_value(node, xfail_lines)
    return xfail_reasons


def get_wrong_xfail_decorator_lines(ast_tree: ast.AST) -> typing.Tuple[typing.Set[int], typing.Set[int]]:
    xfail_reasons = get_xfail_reasons(ast_tree)
    xfail_without_reason = get_xfail_line_numbers(ast_tree)
    xfail_with_empty_reason: typing.Set[int] = set()

    for line, reason in xfail_reasons.items():
        xfail_without_reason.remove(line)
        if not reason:
            xfail_with_empty_reason.add(line)

    return xfail_with_empty_reason, xfail_without_reason

import ast

XFAIL_MARK_NAME = 'xfail'
REASON_ARGUMENT_NAME = 'reason'


def is_xfail_mark(node: ast.AST) -> bool:
    return isinstance(node, ast.Attribute) and node.attr == XFAIL_MARK_NAME


def get_reason_keyword(call: ast.Call) -> ast.keyword | None:
    for keyword in call.keywords:
        if keyword.arg == REASON_ARGUMENT_NAME:
            return keyword
    return None


def is_empty_reason(reason: ast.expr) -> bool:
    """
    Tells whether an xfail reason is provably empty.

    Only literals can be judged: a reason built from a variable, a call or an
    f-string is considered filled in, since its value is unknown until runtime.
    """
    return isinstance(reason, ast.Constant) and not reason.value


def get_wrong_xfail_decorator_lines(ast_tree: ast.AST) -> tuple[set[int], set[int]]:
    """
    Collects lines of xfail marks that are not documented well enough.

    Returns lines of marks with an empty reason and lines of marks
    with no reason argument at all, in that order.
    """
    xfail_with_empty_reason: set[int] = set()
    xfail_without_reason: set[int] = set()

    bare_marks: dict[ast.AST, int] = {}
    called_marks: set[ast.AST] = set()

    for node in ast.walk(ast_tree):
        if is_xfail_mark(node):
            bare_marks[node] = node.lineno  # type: ignore[attr-defined]
        elif isinstance(node, ast.Call) and is_xfail_mark(node.func):
            called_marks.add(node.func)

            reason = get_reason_keyword(node)
            if reason is None:
                xfail_without_reason.add(node.lineno)
            elif is_empty_reason(reason.value):
                xfail_with_empty_reason.add(node.lineno)

    for mark, lineno in bare_marks.items():
        if mark not in called_marks:
            xfail_without_reason.add(lineno)

    return xfail_with_empty_reason, xfail_without_reason

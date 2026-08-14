import argparse
import ast
from collections.abc import Generator

ErrorType = tuple[int, int, str]

CheckResult = Generator[ErrorType, None, None]

AnyFunctionDef = ast.FunctionDef | ast.AsyncFunctionDef

Options = argparse.Namespace

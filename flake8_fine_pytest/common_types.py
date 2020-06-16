import typing

ErrorType = typing.Tuple[int, int, str]

CheckResult = typing.Generator[ErrorType, None, None]

import typing

import pytest

import spreadsheet


@pytest.mark.parametrize(
    "input,expected",
    [
        ("=sum([1, 2])", True),
        ("Hello World", False),
        ("Hello=World", False),
        ("=1", True),
    ],
)
def test_is_dynamic(input: str, expected: bool) -> None:
    cell = spreadsheet.Cell()
    cell.set_contents(input)
    assert cell.is_dynamic == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("1", 1),
        ("1.1", 1.1),
        ("TEST", "TEST"),
        ("=sum([1, 2])", 3),
        ("=max([1, 2])", 2),
        ("=min([1, 2])", 1),
        ("=3*4", 12),
        ("=[ i / 3 for i in [3,6,9]]", [1, 2, 3]),
        ("=[ i % 3 for i in [4,7,10]]", [1, 1, 1]),
        ("=None", "N/A"),
    ],
)
def test_value(input: str, expected: typing.Any) -> None:
    cell = spreadsheet.Cell()
    cell.set_contents(input)
    assert cell.value == expected


@pytest.mark.parametrize(
    "input,exception,message",
    [
        # Methods not on the whitelist are not allowed
        ("=next(())", PermissionError, "Method not in whitelist: ['next']!!"),
        # Imports are not allowed
        ("=import json", SyntaxError, "invalid syntax (<string>, line 1)"),
    ],
)
def test_blacklisted(input: str, exception: typing.Any, message: str) -> None:
    cell = spreadsheet.Cell()
    with pytest.raises(exception) as exc_info:
        cell.set_contents(input)
    assert str(exc_info.value) == message

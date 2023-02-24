import pytest
import spreadsheet


@pytest.mark.parametrize(
    "input,expected",
    [
        ("=SUM(1, 2)", True),
        ("Hello World", False),
        ("Hello=World", False),
        ("=1", True),
    ],
)
def test_is_dynamic(input, expected):
    cell = spreadsheet.Cell(input)
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
def test_value(input, expected):
    cell = spreadsheet.Cell(input)
    cell.eval()
    assert cell.value == expected


@pytest.mark.parametrize(
    "input,exception",
    [
        ("=next(())", "Method not in whitelist: ['next']!!"),
    ],
)
def test_blacklisted(input, exception):
    cell = spreadsheet.Cell(input)
    with pytest.raises(PermissionError) as exc_info:
        cell.eval()
    assert str(exc_info.value) == exception

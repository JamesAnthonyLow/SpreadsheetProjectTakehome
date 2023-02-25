import typing

import pytest

import spreadsheet


@pytest.mark.parametrize("input, expected", [("A2", (0, 1)), ("B8", (1, 7))])
def test_cell_key(input: str, expected: typing.Tuple[int, int]) -> None:
    cell_key = spreadsheet.CellKey.from_key_string(input)
    column, row = expected
    assert cell_key.row == row
    assert cell_key.column == column

    cell_key2 = spreadsheet.CellKey.from_row_and_column(
        row=cell_key.row, column=cell_key.column
    )
    assert cell_key2.key_string == input


@pytest.mark.parametrize("input, exception", [("AA3", "Invalid key format")])
def test_bad_key(input: str, exception: str) -> None:
    with pytest.raises(KeyError) as exc_info:
        spreadsheet.CellKey.from_key_string(input)
    assert str(exc_info.value) == f"'{exception}'"

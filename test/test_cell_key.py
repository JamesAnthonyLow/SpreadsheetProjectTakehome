import pytest

import spreadsheet


@pytest.mark.parametrize(
    "input, expected", [("A2", "Column: 0, Row: 1"), ("B8", "Column: 1, Row: 7")]
)
def test_cell_key(input: str, expected: str) -> None:
    cell_key = spreadsheet.CellKey(input)
    assert repr(cell_key) == expected

    cell_key2 = spreadsheet.CellKey(row=cell_key.row, column=cell_key.column)
    assert cell_key2.key_string == input


@pytest.mark.parametrize("input, exception", [("AA3", "Invalid key format")])
def test_bad_key(input: str, exception: str) -> None:
    with pytest.raises(KeyError) as exc_info:
        spreadsheet.CellKey(input)
    assert str(exc_info.value) == f"'{exception}'"

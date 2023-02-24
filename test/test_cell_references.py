import pytest
import spreadsheet


def test_circular_references_disallowed() -> None:
    cell_references = spreadsheet.CellReferences()
    cell_references.update_references(
        spreadsheet.CellKey("A2"), [spreadsheet.CellKey("C2")]
    )
    with pytest.raises(ValueError) as exc_info:
        cell_references.update_references(
            spreadsheet.CellKey("C2"), [spreadsheet.CellKey("A2")]
        )
    assert str(exc_info.value) == "Circular reference detected"


# def test_get_references() -> None:
#     cell_references = spreadsheet.CellReferences()
#     cell_references.add(spreadsheet.CellKey("A2"), spreadsheet.CellKey("C2"))
#     cell_references.add(spreadsheet.CellKey("A2"), spreadsheet.CellKey("D2"))
#     cell_references.add(spreadsheet.CellKey("A2"), spreadsheet.CellKey("F2"))
#     assert list(cell_references.get(spreadsheet.CellKey("A2"))) == ["C2", "D2", "F2"]

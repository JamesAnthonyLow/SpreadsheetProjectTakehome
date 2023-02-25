import typing

import pytest

import spreadsheet


def test_circular_references_disallowed() -> None:
    cell_references = spreadsheet.CellReferences()
    cell_references.update_references(
        spreadsheet.CellKey("A2"), [spreadsheet.CellKey("C2")]
    )
    cell_references.update_references(
        spreadsheet.CellKey("C2"), [spreadsheet.CellKey("B2")]
    )

    with pytest.raises(ValueError) as exc_info:
        cell_references.update_references(
            spreadsheet.CellKey("B2"), [spreadsheet.CellKey("A2")]
        )
    assert str(exc_info.value) == "Circular reference detected"


@pytest.mark.parametrize(
    "updates,expected_to,expected_from",
    [
        (
            [("A2", ["B2", "B3", "B4"]), ("B2", ["C4", "C6"]), ("A2", ["B2"])],
            {"B2": ["A2"], "B3": [], "B4": [], "C4": ["B2"], "C6": ["B2"]},
            {
                "A2": ["B2"],
                "B2": ["C4", "C6"],
                "B3": [],
                "B4": [],
                "C4": [],
                "C6": [],
            },
        )
    ],
)
def test_references_update(
    updates: typing.Tuple[str, typing.List[str]],
    expected_to: typing.Dict[str, typing.List[str]],
    expected_from: typing.Dict[str, typing.List[str]],
) -> None:
    cell_references = spreadsheet.CellReferences()
    for from_, to in updates:
        cell_references.update_references(
            spreadsheet.CellKey(from_), [spreadsheet.CellKey(t) for t in to]
        )
    assert dict(cell_references._to_references) == expected_to
    assert dict(cell_references._from_references) == expected_from

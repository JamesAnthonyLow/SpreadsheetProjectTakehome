import typing

import pytest

import spreadsheet


def test_circular_references_disallowed() -> None:
    cell_references = spreadsheet.CellReferences()
    cell_references.update_references(
        spreadsheet.CellKey.from_key_string("A2"),
        [spreadsheet.CellKey.from_key_string("C2")],
    )
    cell_references.update_references(
        spreadsheet.CellKey.from_key_string("C2"),
        [spreadsheet.CellKey.from_key_string("B2")],
    )

    with pytest.raises(ValueError) as exc_info:
        cell_references.update_references(
            spreadsheet.CellKey.from_key_string("B2"),
            [spreadsheet.CellKey.from_key_string("A2")],
        )
    assert str(exc_info.value) == "Circular reference forbidden!!"


def test_self_reference_disallowed() -> None:
    cell_references = spreadsheet.CellReferences()
    with pytest.raises(ValueError) as exc_info:
        cell_references.update_references(
            spreadsheet.CellKey.from_key_string("C2"),
            [spreadsheet.CellKey.from_key_string("C2")],
        )
    assert str(exc_info.value) == "Self-reference forbidden!!"


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
            spreadsheet.CellKey.from_key_string(from_),
            [spreadsheet.CellKey.from_key_string(t) for t in to],
        )

    def _assert_eq(actual: typing.Any, expected: typing.Any) -> None:
        expected_converted = {
            spreadsheet.CellKey.from_key_string(k): [
                spreadsheet.CellKey.from_key_string(v) for v in values
            ]
            for k, values in expected.items()
        }
        assert dict(actual) == expected_converted

    _assert_eq(cell_references._to_references, expected_to)
    _assert_eq(cell_references._from_references, expected_from)

import collections
import re
import typing

import attr
import prettytable

COLUMNS = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
METHOD_ALLOW_LIST = ["sum", "max", "min", "ref", "join", "format"]
"""
In addition to this allowlist all python expressions 
(i.e., +,-,/,* and list/dictionary comprehensions) are supported

Imports are forbidden
"""


@attr.define(frozen=True)
class CellKey:
    key_string: str
    row: int
    column: int

    @classmethod
    def from_key_string(cls, key_string: str) -> "CellKey":
        result = re.search(r"^([A-Z])([0-9]+)$", key_string)
        if result is None:
            raise KeyError("Invalid key format")
        column_character, row_idx = result.groups()
        column = COLUMNS.index(column_character)
        row = int(row_idx) - 1
        return cls(key_string, row, column)

    @classmethod
    def from_row_and_column(cls, row: int, column: int) -> "CellKey":
        key_string = COLUMNS[column] + str(row + 1)
        return cls(key_string, row, column)

    def __repr__(self) -> str:
        return self.key_string


class Cell:
    def __init__(self) -> None:
        self.contents: str = ""
        self.value: typing.Union[int, float, str] = ""

    @property
    def is_dynamic(self) -> bool:
        return self.contents.startswith("=")

    @staticmethod
    def _ref_placeholder(_: str) -> str:
        """Mostly used for testing only"""
        return ""

    def set_contents(
        self,
        contents: str,
        ref: typing.Callable[[str], typing.Union[int, float, str]] = _ref_placeholder,
    ) -> None:
        self.contents = contents
        self.eval(ref)

    @staticmethod
    def _parse_value(value: str) -> typing.Union[int, float, str]:
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                ...
        return value

    def eval(self, ref: typing.Callable[[str], typing.Union[int, float, str]]) -> None:
        """
        ref method is passed in to allow access to a global state that keeps track of
        what cells reference eachother without forcing the Cell class to have access to the Spreadsheet class
        """
        if not self.is_dynamic:
            self.value = Cell._parse_value(self.contents)
        else:
            compiled = compile(
                filename="<string>", source=self.contents[1:], mode="eval"
            )
            forbidden = [
                name for name in compiled.co_names if name not in METHOD_ALLOW_LIST
            ]
            if len(forbidden) > 0:
                raise PermissionError(f"Method not in allowlist: {forbidden}!!")

            value = eval(compiled, {"ref": ref})
            if value is None:
                value = "N/A"
            self.value = value


MAX_SPREADSHEET_COLUMNS = 26
MAX_SPREADSHEET_ROWS = 20


class CellReferences:
    """
    Bi-Directional mapping of cells that reference other cells and cells that are referenced by those cells
    """

    def __init__(self) -> None:
        # Reference goes to key from value
        self._to_references: typing.Dict[
            CellKey, typing.List[CellKey]
        ] = collections.defaultdict(list)
        # Reference goes from key to value
        self._from_references: typing.Dict[
            CellKey, typing.List[CellKey]
        ] = collections.defaultdict(list)

    def update_references(self, from_: CellKey, to: typing.List[CellKey]) -> None:
        # Detected self reference
        if from_ in to:
            raise ValueError("Self-reference forbidden!!")

        # Detect circular references
        def _dfs(to_cell_key: CellKey) -> None:
            references = self._from_references[to_cell_key]
            if from_ in references:
                raise ValueError("Circular reference forbidden!!")
            for reference in references:
                _dfs(reference)

        for to_cell_key in to:
            _dfs(to_cell_key)
        # Remove old "to" references
        for to_cell_key in self._from_references[from_]:
            self._to_references[to_cell_key].remove(from_)

        # Remove old "from" references
        self._from_references[from_] = []

        # Re-populate references
        for to_cell_key in to:
            self._from_references[from_].append(to_cell_key)
            self._to_references[to_cell_key].append(from_)

    def get_references_to(self, to: CellKey) -> typing.List[CellKey]:
        return self._to_references[to]

    def __repr__(self) -> str:
        return f"{self._to_references} {self._from_references}"


class Spreadsheet:
    def __init__(
        self,
        number_of_columns: int = 10,
        number_of_rows: int = 10,
        cell_width: int = 10,
    ) -> None:
        if number_of_columns > MAX_SPREADSHEET_COLUMNS:
            raise ValueError("Number of columns exceeds max")

        if number_of_rows > MAX_SPREADSHEET_ROWS:
            raise ValueError("Number of rows exceeds max")

        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.cell_width = cell_width
        self.cells = []
        self.cell_references = CellReferences()
        for _ in range(self.number_of_rows):
            row = []
            for _ in range(self.number_of_columns):
                row.append(Cell())
            self.cells.append(row)

    def __setitem__(self, key_string: str, contents: str) -> None:
        cell_key = CellKey.from_key_string(key_string=key_string)

        references = []

        def _ref(key_string: str) -> typing.Union[int, float, str]:
            reference = CellKey.from_key_string(key_string=key_string)
            references.append(reference)
            return self.__getitem__(key_string).value

        self.cells[cell_key.row][cell_key.column].set_contents(contents, ref=_ref)

        # Update references
        self.cell_references.update_references(from_=cell_key, to=references)

        def _eval_cells_referencing(cell_key: CellKey) -> None:
            for reference in self.cell_references.get_references_to(cell_key):

                def _ref(key_string: str) -> typing.Union[int, float, str]:
                    """No need to recalculate cell references, we just need the value"""
                    return self.__getitem__(key_string).value

                self.cells[reference.row][reference.column].eval(_ref)
                _eval_cells_referencing(reference)

        _eval_cells_referencing(cell_key=cell_key)

    def __getitem__(self, key_string: str) -> Cell:
        cell_key = CellKey.from_key_string(key_string=key_string)
        return self.cells[cell_key.row][cell_key.column]

    def __str__(self) -> str:
        headers = COLUMNS[: self.number_of_columns]
        table = prettytable.PrettyTable()
        table.field_names = ["Row"] + headers
        for row_no, row_cells in enumerate(self.cells):
            row = [cell.value for cell in row_cells]
            table.add_row(row=[row_no + 1] + row)
        return f"{table}"

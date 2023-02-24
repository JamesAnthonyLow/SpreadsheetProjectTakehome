import collections
import re
import typing

import prettytable

COLUMNS = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


class CellKey:
    def __init__(
        self,
        key_string: typing.Optional[str] = None,
        row: typing.Optional[int] = None,
        column: typing.Optional[int] = None,
    ) -> None:
        if key_string is not None and row is None and column is None:
            result = re.search(r"^([A-Z])([0-9]+)$", key_string)
            if result is None:
                raise KeyError("Invalid key format")
            column_character, row_idx = result.groups()
            self.key_string = key_string
            self.column = COLUMNS.index(column_character)
            self.row = int(row_idx) - 1
        elif row is not None and column is not None and key_string is None:
            self.column = column
            self.row = row
            self.key_string = COLUMNS[column] + str(self.row + 1)
        else:
            raise ValueError(
                "CellKey must be instantiated with either key_string are or row and column args"
            )

    def __repr__(self) -> str:
        return f"Column: {self.column}, Row: {self.row}"


class Cell:
    def __init__(self, row: int, column: int) -> None:
        self.key = CellKey(row=row, column=column)
        self.contents: str = ""
        self.value: typing.Union[int, float, str] = ""

    @property
    def is_dynamic(self) -> bool:
        return self.contents.startswith("=")

    @staticmethod
    def _ref_placeholder(_: str) -> str:
        return ""

    def set_contents(
        self,
        contents: str,
        ref: typing.Callable[[str], typing.Union[int, float, str]] = _ref_placeholder,
    ) -> None:
        self.contents = contents
        self._eval(ref)

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

    def _eval(self, ref: typing.Callable[[str], typing.Union[int, float, str]]) -> None:
        if not self.is_dynamic:
            self.value = Cell._parse_value(self.contents)
        else:
            method_whitelist = ["sum", "max", "min", "ref"]
            """
            In addition to this whitelist all python expressions 
            (i.e., +,-,/,* and list/dictionary comprehensions) are supported

            Imports are forbidden
            """
            compiled = compile(
                filename="<string>", source=self.contents[1:], mode="eval"
            )
            blacklisted = [
                name for name in compiled.co_names if name not in method_whitelist
            ]
            if len(blacklisted) > 0:
                raise PermissionError(f"Method not in whitelist: {blacklisted}!!")

            value = eval(compiled, {"ref": ref})
            if value is None:
                value = "N/A"
            self.value = value


MAX_SPREADSHEET_COLUMNS = 26
MAX_SPREADSHEET_ROWS = 20


class CellReferences:
    def __init__(self) -> None:
        self._references: typing.Dict[str, typing.List[str]] = collections.defaultdict(
            list
        )

    def get(self, key: CellKey) -> typing.Generator[str, None, None]:
        """
        Returns a generator to ensure there's no unsafe access to the underlying collection
        """
        return (reference for reference in self._references[key.key_string])

    def add(self, key: CellKey, reference: CellKey) -> None:
        def _dfs(reference: CellKey) -> None:
            references = self._references[reference.key_string]
            if key.key_string in references:
                raise ValueError("Circular reference detected")
            for reference in references:
                _dfs(reference)

        _dfs(reference)
        self._references[key.key_string].append(reference.key_string)


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
        for row_idx in range(self.number_of_rows):
            row = []
            for column_idx in range(self.number_of_columns):
                row.append(Cell(row_idx, column_idx))
            self.cells.append(row)

    def __setitem__(self, key_string: str, contents: str) -> None:
        cell_key = CellKey(key_string=key_string)

        def _ref(key_string: str) -> typing.Union[int, float, str]:
            reference = CellKey(key_string=key_string)
            self.cell_references.add(cell_key, reference)
            return self.__getitem__(key_string).value

        self.cells[cell_key.row][cell_key.column].set_contents(contents, ref=_ref)

    def __getitem__(self, key_string: str) -> str:
        cell_key = CellKey(key_string=key_string)
        return self.cells[cell_key.row][cell_key.column]

    def __str__(self) -> str:
        headers = COLUMNS[: self.number_of_columns]
        table = prettytable.PrettyTable()
        table.field_names = ["Row"] + headers
        for row_no, row_cells in enumerate(self.cells):
            row = [cell.value for cell in row_cells]
            table.add_row(row=[row_no + 1] + row)
        return f"{table}"

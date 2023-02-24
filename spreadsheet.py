import re
import typing

import prettytable


class Cell:
    def __init__(self) -> None:
        self.contents: str = ""
        self.value: typing.Union[int, float, str] = ""

    @property
    def is_dynamic(self) -> bool:
        return self.contents.startswith("=")

    def set_contents(self, contents: str) -> None:
        self.contents = contents
        self._eval()

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

    def _eval(self) -> None:
        if not self.is_dynamic:
            self.value = Cell._parse_value(self.contents)
        else:
            method_whitelist = ["sum", "max", "min"]
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

            value = eval(compiled)
            if value is None:
                value = "N/A"
            self.value = value


COLUMNS = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


class CellKey:
    def __init__(self, key_string: str) -> None:
        result = re.search(r"^([A-Z])([0-9]+)$", key_string)
        if result is None:
            raise KeyError("Invalid key format")
        column_character, row_idx = result.groups()
        self.column = COLUMNS.index(column_character)
        self.row = int(row_idx) - 1

    def __repr__(self) -> str:
        return f"Column: {self.column}, Row: {self.row}"


MAX_SPREADSHEET_COLUMNS = 26
MAX_SPREADSHEET_ROWS = 20


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
        for _ in range(self.number_of_rows):
            row = []
            for _ in range(self.number_of_columns):
                row.append(Cell())
            self.cells.append(row)

    def __setitem__(self, key_string: str, contents: str) -> None:
        cell_key = CellKey(key_string=key_string)
        self.cells[cell_key.row][cell_key.column].set_contents(contents)

    def __getitem__(self, key_string: str) -> str:
        cell_key = CellKey(key_string=key_string)
        return self.cells[cell_key.row][cell_key.column].contents

    def __str__(self) -> str:
        headers = COLUMNS[: self.number_of_columns]
        table = prettytable.PrettyTable()
        table.field_names = ["Row"] + headers
        for row_no, row_cells in enumerate(self.cells):
            row = [cell.value for cell in row_cells]
            table.add_row(row=[row_no + 1] + row)
        return f"{table}"

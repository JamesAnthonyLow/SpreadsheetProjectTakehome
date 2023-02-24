import re
import prettytable
import typing


class Cell:
    def __init__(self):
        self._contents: str = ""
        self.value: typing.Optional[typing.Union[int, float, str]] = None

    @property
    def is_dynamic(self) -> bool:
        return self._contents.startswith("=")

    def set_contents(self, _contents: str):
        self._contents: str = _contents

    def _parse_value(value: typing.Optional[str]) -> typing.Union[int, float, str]:
        if value is None:
            return ""
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                ...
        return value

    def eval(self):
        if not self.is_dynamic:
            self.value: typing.Union[int, float, str] = Cell._parse_value(
                self._contents
            )
        else:
            method_whitelist = ["sum", "max", "min"]
            """
            In addition to this whitelist all python expressions 
            (i.e., +,-,/,* and list/dictionary comprehensions) are supported

            Imports are forbidden
            """
            compiled = compile(
                filename="<string>", source=self._contents[1:], mode="eval"
            )
            blacklisted = [
                name for name in compiled.co_names if name not in method_whitelist
            ]
            if len(blacklisted) > 0:
                raise PermissionError(f"Method not in whitelist: {blacklisted}!!")

            value = eval(compiled)
            if value is None:
                value = "N/A"
            self.value: typing.Union[int, float, str] = value


COLUMNS = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


class CellKey:
    def __init__(self, key_string):
        result = re.search(r"^([A-Z])([0-9]+)$", key_string)
        if result is None:
            raise KeyError("Invalid key format")
        column_character, row_idx = result.groups()
        self.column = COLUMNS.index(column_character)
        self.row = int(row_idx) - 1

    def __repr__(self):
        return f"Column: {self.column}, Row: {self.row}"


MAX_SPREADSHEET_COLUMNS = 26
MAX_SPREADSHEET_ROWS = 20


class Spreadsheet:
    def __init__(
        self,
        number_of_columns: int = 10,
        number_of_rows: int = 10,
        cell_width: int = 10,
    ):
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

    def __setitem__(self, key_string: str, contents: str):
        cell_key = CellKey(key_string=key_string)
        self.cells[cell_key.row][cell_key.column].set_contents(contents)

    def __str__(self):
        headers = COLUMNS[: self.number_of_columns]
        table = prettytable.PrettyTable()
        table.field_names = ["Row"] + headers
        for row_no, row_cells in enumerate(self.cells):
            row = []
            for cell in row_cells:
                if cell.value is None:
                    cell.eval()
                row.append(cell.value)
            table.add_row(row=[row_no + 1] + row)
        return f"{table}"

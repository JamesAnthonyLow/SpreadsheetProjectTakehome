import typing

import pytest

import spreadsheet


@pytest.mark.parametrize(
    "changes,expected",
    [
        (
            [],
            """+-----+---+---+---+---+---+---+---+---+---+---+
| Row | A | B | C | D | E | F | G | H | I | J |
+-----+---+---+---+---+---+---+---+---+---+---+
|  1  |   |   |   |   |   |   |   |   |   |   |
|  2  |   |   |   |   |   |   |   |   |   |   |
|  3  |   |   |   |   |   |   |   |   |   |   |
|  4  |   |   |   |   |   |   |   |   |   |   |
|  5  |   |   |   |   |   |   |   |   |   |   |
|  6  |   |   |   |   |   |   |   |   |   |   |
|  7  |   |   |   |   |   |   |   |   |   |   |
|  8  |   |   |   |   |   |   |   |   |   |   |
|  9  |   |   |   |   |   |   |   |   |   |   |
|  10 |   |   |   |   |   |   |   |   |   |   |
+-----+---+---+---+---+---+---+---+---+---+---+""",
        ),
        (
            [("B2", "2")],
            """+-----+---+---+---+---+---+---+---+---+---+---+
| Row | A | B | C | D | E | F | G | H | I | J |
+-----+---+---+---+---+---+---+---+---+---+---+
|  1  |   |   |   |   |   |   |   |   |   |   |
|  2  |   | 2 |   |   |   |   |   |   |   |   |
|  3  |   |   |   |   |   |   |   |   |   |   |
|  4  |   |   |   |   |   |   |   |   |   |   |
|  5  |   |   |   |   |   |   |   |   |   |   |
|  6  |   |   |   |   |   |   |   |   |   |   |
|  7  |   |   |   |   |   |   |   |   |   |   |
|  8  |   |   |   |   |   |   |   |   |   |   |
|  9  |   |   |   |   |   |   |   |   |   |   |
|  10 |   |   |   |   |   |   |   |   |   |   |
+-----+---+---+---+---+---+---+---+---+---+---+""",
        ),
        (
            [("B2", "=sum([3, 4])"), ("I9", "=5*2")],
            """+-----+---+---+---+---+---+---+---+---+----+---+
| Row | A | B | C | D | E | F | G | H | I  | J |
+-----+---+---+---+---+---+---+---+---+----+---+
|  1  |   |   |   |   |   |   |   |   |    |   |
|  2  |   | 7 |   |   |   |   |   |   |    |   |
|  3  |   |   |   |   |   |   |   |   |    |   |
|  4  |   |   |   |   |   |   |   |   |    |   |
|  5  |   |   |   |   |   |   |   |   |    |   |
|  6  |   |   |   |   |   |   |   |   |    |   |
|  7  |   |   |   |   |   |   |   |   |    |   |
|  8  |   |   |   |   |   |   |   |   |    |   |
|  9  |   |   |   |   |   |   |   |   | 10 |   |
|  10 |   |   |   |   |   |   |   |   |    |   |
+-----+---+---+---+---+---+---+---+---+----+---+""",
        ),
        (
            [("D2", '="Hello" + " World"')],
            """+-----+---+---+---+-------------+---+---+---+---+---+---+
| Row | A | B | C |      D      | E | F | G | H | I | J |
+-----+---+---+---+-------------+---+---+---+---+---+---+
|  1  |   |   |   |             |   |   |   |   |   |   |
|  2  |   |   |   | Hello World |   |   |   |   |   |   |
|  3  |   |   |   |             |   |   |   |   |   |   |
|  4  |   |   |   |             |   |   |   |   |   |   |
|  5  |   |   |   |             |   |   |   |   |   |   |
|  6  |   |   |   |             |   |   |   |   |   |   |
|  7  |   |   |   |             |   |   |   |   |   |   |
|  8  |   |   |   |             |   |   |   |   |   |   |
|  9  |   |   |   |             |   |   |   |   |   |   |
|  10 |   |   |   |             |   |   |   |   |   |   |
+-----+---+---+---+-------------+---+---+---+---+---+---+""",
        ),
        (
            [
                ("B2", "=sum([3, 4])"),
                ("I9", "=5*2"),
                ("J3", '=ref("B2")'),
                ("F5", '=ref("J3") + 1'),
                ("B2", '=ref("I9") - 2'),
            ],
            """+-----+---+---+---+---+---+---+---+---+----+---+
| Row | A | B | C | D | E | F | G | H | I  | J |
+-----+---+---+---+---+---+---+---+---+----+---+
|  1  |   |   |   |   |   |   |   |   |    |   |
|  2  |   | 8 |   |   |   |   |   |   |    |   |
|  3  |   |   |   |   |   |   |   |   |    | 8 |
|  4  |   |   |   |   |   |   |   |   |    |   |
|  5  |   |   |   |   |   | 9 |   |   |    |   |
|  6  |   |   |   |   |   |   |   |   |    |   |
|  7  |   |   |   |   |   |   |   |   |    |   |
|  8  |   |   |   |   |   |   |   |   |    |   |
|  9  |   |   |   |   |   |   |   |   | 10 |   |
|  10 |   |   |   |   |   |   |   |   |    |   |
+-----+---+---+---+---+---+---+---+---+----+---+""",
        ),
        (
            [
                ("A3", "3"),
                ("C6", "=sum([2,3])"),
                ("D6", '=ref("C6")'),
                ("C6", "3"),
            ],
            """+-----+---+---+---+---+---+---+---+---+---+---+
| Row | A | B | C | D | E | F | G | H | I | J |
+-----+---+---+---+---+---+---+---+---+---+---+
|  1  |   |   |   |   |   |   |   |   |   |   |
|  2  |   |   |   |   |   |   |   |   |   |   |
|  3  | 3 |   |   |   |   |   |   |   |   |   |
|  4  |   |   |   |   |   |   |   |   |   |   |
|  5  |   |   |   |   |   |   |   |   |   |   |
|  6  |   |   | 3 | 3 |   |   |   |   |   |   |
|  7  |   |   |   |   |   |   |   |   |   |   |
|  8  |   |   |   |   |   |   |   |   |   |   |
|  9  |   |   |   |   |   |   |   |   |   |   |
|  10 |   |   |   |   |   |   |   |   |   |   |
+-----+---+---+---+---+---+---+---+---+---+---+""",
        ),
    ],
)
def test_pretty_print(
    changes: typing.List[typing.Tuple[str, str]], expected: str
) -> None:
    sheet = spreadsheet.Spreadsheet()
    for cell_key, value in changes:
        sheet[cell_key] = value
    assert f"{sheet}" == expected

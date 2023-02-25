# My Spreadsheet

This project can be run using [Docker](https://www.docker.com/) and should require no other dependencies (tested on Macbook M1).

To run, execute:
```
$ ./scripts/run.sh
```

This will build the Docker image **spreadsheet_project_image** and run a container that opens a prompt (implemented using the Python "[Cmd](https://docs.python.org/3/library/cmd.html)" class):

```
 Welcome to My Spreadsheet. Type help or ? to list commands
(spreadsheet)
```

To print out the current state of the spreadsheet use the **print** command:

```
(spreadsheet) print
+-----+---+---+---+---+---+---+---+---+---+---+
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
+-----+---+---+---+---+---+---+---+---+---+---+
```

To set a cell in the spreadsheet use the **set** command:

```
(spreadsheet) set A6 4
+-----+---+---+---+---+---+---+---+---+---+---+
| Row | A | B | C | D | E | F | G | H | I | J |
+-----+---+---+---+---+---+---+---+---+---+---+
|  1  |   |   |   |   |   |   |   |   |   |   |
|  2  |   |   |   |   |   |   |   |   |   |   |
|  3  |   |   |   |   |   |   |   |   |   |   |
|  4  |   |   |   |   |   |   |   |   |   |   |
|  5  |   |   |   |   |   |   |   |   |   |   |
|  6  | 4 |   |   |   |   |   |   |   |   |   |
|  7  |   |   |   |   |   |   |   |   |   |   |
|  8  |   |   |   |   |   |   |   |   |   |   |
|  9  |   |   |   |   |   |   |   |   |   |   |
|  10 |   |   |   |   |   |   |   |   |   |   |
+-----+---+---+---+---+---+---+---+---+---+---+
```
Functions are implemented using python3 itself! (see [compile](https://docs.python.org/3/library/functions.html#compile) and [eval](https://docs.python.org/3/library/functions.html#eval))

```
(spreadsheet) set D6 =(4*8)/2
+-----+---+---+---+------+---+---+---+---+---+---+
| Row | A | B | C |  D   | E | F | G | H | I | J |
+-----+---+---+---+------+---+---+---+---+---+---+
|  1  |   |   |   |      |   |   |   |   |   |   |
|  2  |   |   |   |      |   |   |   |   |   |   |
|  3  |   |   |   |      |   |   |   |   |   |   |
|  4  |   |   |   |      |   |   |   |   |   |   |
|  5  |   |   |   |      |   |   |   |   |   |   |
|  6  | 4 |   |   | 16.0 |   |   |   |   |   |   |
|  7  |   |   |   |      |   |   |   |   |   |   |
|  8  |   |   |   |      |   |   |   |   |   |   |
|  9  |   |   |   |      |   |   |   |   |   |   |
|  10 |   |   |   |      |   |   |   |   |   |   |
+-----+---+---+---+------+---+---+---+---+---+---+
```

This is implemented using an allowlist with the following python functions (see **spreadsheet.py:METHOD_ALLOW_LIST**):

* **sum**
* **max**
* **min**
* **join**
* **format**

All expressions are supported such as +, -, /, % and list comprehensions. Imports are not allowed.

References are implemented using the **ref** method, like so:
```
(spreadsheet) set C2 =ref("D6")
+-----+---+---+------+------+---+---+---+---+---+---+
| Row | A | B |  C   |  D   | E | F | G | H | I | J |
+-----+---+---+------+------+---+---+---+---+---+---+
|  1  |   |   |      |      |   |   |   |   |   |   |
|  2  |   |   | 16.0 |      |   |   |   |   |   |   |
|  3  |   |   |      |      |   |   |   |   |   |   |
|  4  |   |   |      |      |   |   |   |   |   |   |
|  5  |   |   |      |      |   |   |   |   |   |   |
|  6  | 4 |   |      | 16.0 |   |   |   |   |   |   |
|  7  |   |   |      |      |   |   |   |   |   |   |
|  8  |   |   |      |      |   |   |   |   |   |   |
|  9  |   |   |      |      |   |   |   |   |   |   |
|  10 |   |   |      |      |   |   |   |   |   |   |
+-----+---+---+------+------+---+---+---+---+---+---+
```

When the referenced cell is updated all cells referencing that cell are re-evaluated.

Nested functions are also supported:

```
(spreadsheet) set E3 =sum([ref("D6"), ref("A6")*2])
+-----+---+---+------+------+------+---+---+---+---+---+
| Row | A | B |  C   |  D   |  E   | F | G | H | I | J |
+-----+---+---+------+------+------+---+---+---+---+---+
|  1  |   |   |      |      |      |   |   |   |   |   |
|  2  |   |   | 16.0 |      |      |   |   |   |   |   |
|  3  |   |   |      |      | 24.0 |   |   |   |   |   |
|  4  |   |   |      |      |      |   |   |   |   |   |
|  5  |   |   |      |      |      |   |   |   |   |   |
|  6  | 4 |   |      | 16.0 |      |   |   |   |   |   |
|  7  |   |   |      |      |      |   |   |   |   |   |
|  8  |   |   |      |      |      |   |   |   |   |   |
|  9  |   |   |      |      |      |   |   |   |   |   |
|  10 |   |   |      |      |      |   |   |   |   |   |
+-----+---+---+------+------+------+---+---+---+---+---+
```

### Directory Structure
* [main.py](./main.py) - implements the console/prompt using the Python "[Cmd](https://docs.python.org/3/library/cmd.html)" class
* [spreadsheet.py](./spreadsheet.py) - source code implementing "Spreadsheet" and "Cell" classes
* [test](./test) - test directory housing pytest implemented unit tests
* [scripts](./scripts) - contains helpful shell scripts that build and run the docker container to achieve various objectives such as [linting](./scripts/lint.sh), [testing](./scripts/test.sh), [updating requirements.txt using pip-tools](./scripts/update_requirements.sh) and [running the spreadsheet prompt](./scripts/run.sh)


### Limitations (WIP)

Currently the spreadsheet app only supports editing the spreadsheet in memory.  There is no on-disk representation so when you exit the spreadsheet app you lose whatever progress you had made.  Saving the spreadsheet to a CSV of the users choice would likely be somewhat trivial.  Additionally, the spreadsheet is restricted to 10 columns and 10 rows.  26 columns and N number of rows is supported in the implementation of the "Spreadsheet" class but any more columns than 26 would require a slight refactor to the "CellKey" class.  Another nice addition would be the ability to reference ranges (i.e, ```=sum(ref("A1:A8"))```) which should be possible with some minor refactors to the reference code.
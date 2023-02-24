import cmd

import spreadsheet


class SpreadsheetController(cmd.Cmd):
    intro = "Welcome to My Spreadsheet. Type help or ? to list commands"
    prompt = "(spreadsheet) "
    file = None

    def onecmd(self, line: str) -> bool:
        permitted_errors = (
            KeyError,
            ValueError,
            TypeError,
            SyntaxError,
            PermissionError,
        )
        try:
            return super().onecmd(line)
        except permitted_errors as e:
            print(e)
            return False

    def do_print(self, _args: str) -> None:
        "Print out the current contents of the spreadsheet"
        print(spreadsheet.SHEET)

    def do_set(self, args: str) -> None:
        "Set the contents of a spreadsheet cell: [CELL-KEY] [CONTENTS]"
        cell_key, contents = args.split(" ")
        spreadsheet.Sheet[cell_key] = contents
        print(spreadsheet.Sheet)

    def do_get(self, cell_key: str) -> None:
        "Get the un-evaluated contents of a spreadsheet cell"
        print(spreadsheet.Sheet[cell_key].contents)

    def do_exit(self, _args: str) -> None:
        "Exit this prompt"
        exit()


if __name__ == "__main__":
    SpreadsheetController().cmdloop()

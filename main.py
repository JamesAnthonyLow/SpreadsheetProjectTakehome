import cmd

import spreadsheet

sheet = spreadsheet.Spreadsheet()


class SpreadsheetController(cmd.Cmd):
    intro = "Welcome to My Spreadsheet. Type help or ? to list commands"
    prompt = "(spreadsheet) "
    file = None

    def onecmd(self, line):
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
        print(sheet)

    def do_set(self, args: str) -> None:
        "Set the contents of a spreadsheet cell: [CELL-KEY] [CONTENTS]"
        cell_key, contents = args.split(" ")
        sheet[cell_key] = contents
        print(sheet)

    def do_get(self, cell_key: str) -> None:
        "Get the un-evaluated contents of a spreadsheet cell"
        print(sheet[cell_key])

    def do_exit(self, _args: str) -> None:
        "Exit this prompt"
        exit()


if __name__ == "__main__":
    SpreadsheetController().cmdloop()

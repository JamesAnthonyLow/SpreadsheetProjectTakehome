import cmd

import spreadsheet

sheet = spreadsheet.Spreadsheet()


class SpreadsheetController(cmd.Cmd):
    intro = "Welcome to My Spreadsheet. Type help or ? to list commands"
    prompt = "(spreadsheet) "
    file = None

    def do_print(self, _args: str) -> None:
        print(sheet)

    def do_set(self, args: str) -> None:
        cell_key, contents = args.split(" ")
        sheet[cell_key] = contents


if __name__ == "__main__":
    SpreadsheetController().cmdloop()

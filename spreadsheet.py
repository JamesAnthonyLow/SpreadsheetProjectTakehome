import typing


class Cell:
    def __init__(self, contents: str):
        self._contents: str = contents
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

from util.Generator import Generator
from util.Scope import Scope
from util.Symbol import Value
from util.Types import Type


class Expression:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def execute(self, scope: Scope, generator: Generator) -> Value:
        return Value(0, False, Type.Int, "", "")

from util.Generator import Generator
from util.Scope import Scope


class Instruction:
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    def execute(self, scope: Scope, generator: Generator) -> any:
        return None

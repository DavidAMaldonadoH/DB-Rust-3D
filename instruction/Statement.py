from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Statement(Instruction):
    def __init__(self, line: int, column: int, code: list[Instruction]):
        super().__init__(line, column)
        self.code = code
        self.name = "Local"

    def setName(self, name: str):
        self.name = name

    def execute(self, scope: Scope, generator: Generator) -> any:
        new_scope = Scope(scope, self.name)
        for instruction in self.code:
            retorno = instruction.execute(new_scope, generator)
        if scope.size < new_scope.size:
            generator.addExpression("P", "P", str(new_scope.size - scope.size), "-")

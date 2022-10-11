from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Statement(Instruction):
    def __init__(self, line: int, column: int, code: list[Instruction]):
        super().__init__(line, column)
        self.code = code
        self.name = "Local"
        self.size = 0
        self.parameters = []

    def setName(self, name: str):
        self.name = name

    def execute(self, scope: Scope, generator: Generator) -> any:
        new_scope = Scope(scope, self.name)
        new_scope.size += self.size
        for parameter in self.parameters:
            new_temp = generator.newTemp()
            generator.addExpression(new_temp, "P", str(new_scope.size), "+")
            new_temp2 = generator.newTemp()
            generator.addGetStack(new_temp2, new_temp)
            new_scope.saveVariable(
                parameter["name"],
                parameter["type"],
                parameter["mut"],
                self.line,
                self.column,
            )
        for instruction in self.code:
            retorno = instruction.execute(new_scope, generator)
        if scope.size < new_scope.size:
            # generator.addExpression("P", "P", str(new_scope.size - scope.size), "-")
            self.size = new_scope.size - scope.size
        if retorno is not None:
            return retorno

from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Default(Instruction):
    def __init__(self, line: int, column: int, code: Instruction):
        super().__init__(line, column)
        self.code = code

    def execute(self, scope: Scope, generator: Generator) -> any:
        retorno = self.code.execute(scope, generator)
        if retorno is not None:
            return retorno

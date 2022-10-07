from util.Error import ERRORS_, Error
from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Break(Instruction):
    def __init__(self, line: int, column: int):
        super().__init__(line, column)

    def execute(self, scope: Scope, generator: Generator) -> any:
        if generator.display.display_ptr == 0:
            err = Error(
                self.line,
                self.column,
                "No se puede usar `break` fuera de un ciclo",
                scope.name,
            )
            ERRORS_.append(err)
            return
        generator.addGoto(generator.getDisplayPtr().salida)
        generator.getDisplayPtr().contB += 1

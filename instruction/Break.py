from typing import Optional
from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Break(Instruction):
    def __init__(self, line: int, column: int, expr: Optional[Expression]):
        super().__init__(line, column)
        self.expr = expr

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
        if self.expr is not None:
            retorno = self.expr.execute(scope, generator)
            generator.addSetStack("P", retorno.value)
        generator.addGoto(generator.getDisplayPtr().salida)
        generator.getDisplayPtr().contB += 1
        if self.expr is not None:
            return retorno

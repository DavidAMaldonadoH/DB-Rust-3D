from typing import Optional
from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Match(Instruction):
    def __init__(
        self,
        line: int,
        column: int,
        expr: Expression,
        cases: list[Instruction],
        default: Optional[Instruction],
    ):
        super().__init__(line, column)
        self.expr = expr
        self.cases = cases
        self.default = default

    def execute(self, scope: Scope, generator: Generator) -> any:
        new_label = generator.newLabel()
        generator.display.nextPtr()
        generator.getDisplayPtr().salida = new_label
        value = self.expr.execute(scope, generator)
        for case in self.cases:
            case.expr = value.value
            retorno = case.execute(scope, generator)
        if self.default is not None:
            retorno = self.default.execute(scope, generator)
        generator.addLabel(new_label)
        generator.display.prevPtr()
        if retorno is not None:
            return retorno

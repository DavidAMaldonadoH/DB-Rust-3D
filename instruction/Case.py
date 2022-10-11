from util.Expression import Expression
from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Case(Instruction):
    def __init__(
        self, line: int, column: int, exprs: list[Expression], code: Instruction
    ):
        super().__init__(line, column)
        self.exprs = exprs
        self.code = code
        self.expr = "0"

    def execute(self, scope: Scope, generator: Generator) -> any:
        true_label = generator.newLabel()
        false_label = generator.newLabel()
        for i, expr in enumerate(self.exprs):
            value = expr.execute(scope, generator)
            if i == len(self.exprs) - 1:
                generator.addIf(self.expr, value.value, "!=", false_label)
            else:
                generator.addIf(self.expr, value.value, "==", true_label)
        generator.addLabel(true_label)
        retorno = self.code.execute(scope, generator)
        generator.addGoto(generator.getDisplayPtr().salida)
        generator.addLabel(false_label)
        if retorno is not None:
            return retorno

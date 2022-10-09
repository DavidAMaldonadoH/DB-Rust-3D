from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Return(Instruction):
    def __init__(self, line, column, expr):
        super().__init__(line, column)
        self.expr = expr

    def execute(self, scope: Scope, generator: Generator) -> any:
        if self.expr is not None:
            value = self.expr.execute(scope, generator)
            generator.addSetStack("P", value.value)
            return value

from util.Expression import Expression
from util.Generator import Generator
from util.Scope import Scope
from util.Symbol import Value
from util.Types import Type


class ToString(Expression):
    def __init__(self, line: int, column: int, expr: Expression):
        super().__init__(line, column)
        self.expr = expr

    def execute(self, scope: Scope, generator: Generator) -> Value:
        expr = self.expr.execute(scope, generator)
        return Value(expr.value, False, Type.String, "", "")

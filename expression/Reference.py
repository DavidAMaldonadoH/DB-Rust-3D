from util.Expression import Expression
from util.Generator import Generator
from util.Types import Type
from util.Scope import Scope
from util.Symbol import Value


class Reference(Expression):
    def __init__(self, line: int, column: int, expression: Expression):
        super().__init__(line, column)
        self.expression = expression

    def execute(self, scope: Scope, generator: Generator) -> Value:
        expr = self.expression.execute(scope, generator)
        if expr.getType() == Type.String:
            return Value(
                expr.value, expr.is_temp, Type.Str, expr.true_label, expr.false_label
            )
        else:
            return Value(
                expr.value, expr.is_temp, expr.type, expr.true_label, expr.false_label
            )

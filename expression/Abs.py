from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Types import Type
from util.Symbol import Value
from util.Scope import Scope


class Abs(Expression):
    def __init__(
        self,
        line: int,
        column: int,
        expr: Expression,
    ):
        super().__init__(line, column)
        self.expr = expr

    def execute(self, scope: Scope, generator: Generator) -> Value:
        expr = self.expr.execute(scope, generator)
        if (
            expr.getType() != Type.F64
            and expr.getType() != Type.I64
            and expr.getType() != Type.Int
        ):
            err = Error(
                self.line,
                self.column,
                f"Los tipos no coinciden: se experaba `i64` o `f64`, se encontro {expr.getType().fullname}",
                scope.name,
            )
            ERRORS_.append(err)
            return
        generator.addExpression("P", "P", str(scope.size), "+")
        new_temp = generator.newTemp()
        t1 = generator.newTemp()
        generator.addExpression(t1, "P", "1", "+")
        generator.addSetStack(t1, expr.getValue())
        generator.addCall("absolute")
        generator.addGetStack(new_temp, "P")
        generator.addExpression("P", "P", str(scope.size), "-")
        return Value(new_temp, True, expr.getType(), [], [])

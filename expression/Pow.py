from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Symbol import Value
from util.Types import Type
from util.Scope import Scope


class Pow(Expression):
    def __init__(
        self, line: int, column: int, left: Expression, right: Expression, type: Type
    ) -> None:
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.type = type

    def execute(self, scope: Scope, generator: Generator) -> Value:
        left_op = self.left.execute(scope, generator)
        right_op = self.right.execute(scope, generator)
        if self.type == Type.I64 and (
            left_op.getType() == Type.F64 or right_op.getType() == Type.F64
        ):
            err = Error(
                self.line,
                self.column,
                f"Se esperaba `i64`, se encontro float",
                scope.name,
            )
            ERRORS_.append(err)
            return

        if self.type == Type.F64 and (
            left_op.getType() == Type.Int
            or right_op.getType() == Type.Int
            or left_op.getType() == Type.I64
            or right_op.getType() == Type.I64
        ):
            err = Error(
                self.line,
                self.column,
                f"Se esperaba `f64`, se encontro integer",
                scope.name,
            )
            ERRORS_.append(err)
            return

        if (
            (left_op.getType() == Type.Int or left_op.getType() == Type.I64)
            and (right_op.getType() == Type.Int or right_op.getType() == Type.I64)
        ) or (left_op.getType() == Type.F64 and right_op.getType() == Type.F64):
            generator.addExpression("P", "P", str(scope.size), "+")
            new_temp = generator.newTemp()
            t1 = generator.newTemp()
            generator.addExpression(t1, "P", "1", "+")
            generator.addSetStack(t1, left_op.getValue())
            t2 = generator.newTemp()
            generator.addExpression(t2, "P", "2", "+")
            generator.addSetStack(t2, right_op.getValue())
            generator.addCall("power")
            generator.addGetStack(new_temp, "P")
            generator.addExpression("P", "P", str(scope.size), "-")
            return Value(new_temp, True, self.type, [], [])
        else:
            err = Error(
                self.line,
                self.column,
                f"No se puede potenciar {left_op.type.fullname} por un {right_op.type.fullname}",
                scope.name,
            )
            ERRORS_.append(err)
            return

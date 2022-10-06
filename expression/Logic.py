from typing import Optional
from util.Error import Error, ERRORS_
from util.Expression import Expression
from util.Scope import Scope
from util.Generator import Generator
from util.Symbol import Value
from util.Types import Type


class Logic(Expression):
    def __init__(
        self,
        line: int,
        column: int,
        left: Optional[Expression],
        right: Expression,
        operator: str,
        unary: bool = False,
    ) -> None:
        super().__init__(line, column)
        self.left = left
        self.right = right
        self.operator = operator
        self.unary = unary

    def execute(self, scope: Scope, generator: Generator) -> Value:
        if self.operator == "!":
            right_op = self.right.execute(scope, generator)
            if right_op.type != Type.Bool:
                err = Error(
                    self.line,
                    self.column,
                    f"El operador {self.operator} solo puede ser aplicado a booleanos",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            return Value(
                right_op.value,
                right_op.is_temp,
                right_op.type,
                right_op.false_label,
                right_op.true_label,
            )
        elif self.operator == "&&":
            left_op = self.left.execute(scope, generator)
            for label in left_op.true_label:
                generator.addLabel(label)
            right_op = self.right.execute(scope, generator)
            if left_op.type != Type.Bool or right_op.type != Type.Bool:
                err = Error(
                    self.line,
                    self.column,
                    f"El operador {self.operator} solo puede ser aplicado a booleanos",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            false_label: list[str] = []
            for l in left_op.false_label:
                false_label.append(l)
            for l in right_op.false_label:
                false_label.append(l)
            return Value(
                "",
                False,
                Type.Bool,
                right_op.true_label,
                false_label,
            )
        else:
            left_op = self.left.execute(scope, generator)
            for label in left_op.false_label:
                generator.addLabel(label)
            right_op = self.right.execute(scope, generator)
            if left_op.type != Type.Bool or right_op.type != Type.Bool:
                err = Error(
                    self.line,
                    self.column,
                    f"El operador {self.operator} solo puede ser aplicado a booleanos",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            true_label: list[str] = []
            for l in left_op.true_label:
                true_label.append(l)
            for l in right_op.true_label:
                true_label.append(l)
            return Value(
                "",
                False,
                Type.Bool,
                true_label,
                right_op.false_label,
            )

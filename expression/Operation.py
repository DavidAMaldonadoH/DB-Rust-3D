from typing import Optional
from util.DominantType import REL_TYPE, RESTO_TYPE, SUMA_TYPE, UNARY_TYPE
from util.Error import Error, ERRORS_
from util.Expression import Expression
from util.Scope import Scope
from util.Generator import Generator
from util.Symbol import Value
from util.Types import Type


class Operation(Expression):
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
        if self.unary:
            right_op = self.right.execute(scope, generator)
        else:
            left_op = self.left.execute(scope, generator)
            right_op = self.right.execute(scope, generator)

        dominant_type: Type

        if self.operator == "+":
            new_temp = generator.newTemp()
            dominant_type = SUMA_TYPE[left_op.type.value][right_op.type.value]
            if dominant_type == Type.Null:
                err = Error(
                    self.line,
                    self.column,
                    f"El operador {self.operator} no puede ser aplicado a los tipos {left_op.type.fullname} y {right_op.type.fullname}",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            generator.addExpression(
                new_temp, left_op.value, right_op.value, self.operator
            )
            return Value(new_temp, True, left_op.type, "", "")
        elif (
            self.operator == "-"
            or self.operator == "*"
            or self.operator == "/"
            or self.operator == "%"
        ):
            new_temp = generator.newTemp()
            if self.unary:
                dominant_type = UNARY_TYPE[right_op.type.value]
                left_value = ""
            else:
                dominant_type = RESTO_TYPE[left_op.type.value][right_op.type.value]
                left_value = left_op.value
            if dominant_type == Type.Null:
                err = Error(
                    self.line,
                    self.column,
                    f"El operador {self.operator} no puede ser aplicado a los tipos {left_op.type.fullname} y {right_op.type.fullname}",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            if self.operator == "%":
                t1 = generator.newTemp()
                generator.addExpression(t1, "P", "1", "+")
                generator.addSetStack(t1, left_value)
                t2 = generator.newTemp()
                generator.addExpression(t2, "P", "2", "+")
                generator.addSetStack(t2, right_op.value)
                generator.addCall("module")
                generator.addGetStack(new_temp, "P")
            else:
                generator.addExpression(
                    new_temp, left_value, right_op.value, self.operator
                )
            return Value(new_temp, True, right_op.type, "", "")
        else:
            dominant_type = REL_TYPE[left_op.type.value][right_op.type.value]
            if dominant_type == Type.Null:
                err = Error(
                    self.line,
                    self.column,
                    f"El operador {self.operator} no puede ser aplicado a los tipos {left_op.type.fullname} y {right_op.type.fullname}",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            true_label = generator.newLabel()
            false_label = generator.newLabel()

            generator.addIf(left_op.value, right_op.value, self.operator, true_label)
            generator.addGoto(false_label)

            return Value("", False, Type.Bool, [true_label], [false_label])

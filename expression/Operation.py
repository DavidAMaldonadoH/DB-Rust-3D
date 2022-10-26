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
                    f"No se puede sumar `{{{right_op.type.fullname}}}` a un `{left_op.type.fullname}`",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            if dominant_type == Type.String:
                generator.addExpression("P", "P", str(scope.size), "+")
                t1 = generator.newTemp()
                t2 = generator.newTemp()
                generator.addExpression(t1, "P", "1", "+")
                generator.addSetStack(t1, left_op.value)
                generator.addExpression(t2, "P", "2", "+")
                generator.addSetStack(t2, right_op.value)
                generator.addCall("concatenate")
                generator.addGetStack(new_temp, "P")
                generator.addExpression("P", "P", str(scope.size), "-")
            else:
                generator.addExpression(
                    new_temp, left_op.value, right_op.value, self.operator
                )
            return Value(new_temp, True, left_op.type, "", "")
        elif self.operator == "-" or self.operator == "*":
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
            generator.addExpression(new_temp, left_value, right_op.value, self.operator)
            return Value(new_temp, True, dominant_type, "", "")
        elif self.operator == "/":
            new_temp = generator.newTemp()
            dominant_type = RESTO_TYPE[left_op.type.value][right_op.type.value]
            if dominant_type == Type.Null:
                err = Error(
                    self.line,
                    self.column,
                    f"No se puede dividir `{{{right_op.type.fullname}}}` por un `{left_op.type.fullname}`",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            label1 = generator.newLabel()
            label2 = generator.newLabel()
            label3 = generator.newLabel()
            generator.addIf(right_op.value, "0", "==", label1)
            generator.addGoto(label2)
            generator.addLabel(label1)
            generator.addCall("mathError")
            generator.addAssignation(new_temp, "0")
            generator.addGoto(label3)
            generator.addLabel(label2)
            if dominant_type == Type.I64 or dominant_type == Type.Int:
                generator.addExpression(
                    new_temp, "(int)" + left_op.value, right_op.value, self.operator
                )
            else:
                generator.addExpression(
                    new_temp, left_op.value, right_op.value, self.operator
                )
            generator.addLabel(label3)
            return Value(new_temp, True, dominant_type, "", "")
        elif self.operator == "%":
            dominant_type = RESTO_TYPE[left_op.type.value][right_op.type.value]
            if dominant_type == Type.Null:
                err = Error(
                    self.line,
                    self.column,
                    f"No se puede aplicar mod `{{{right_op.type.fullname}}}` a un `{left_op.type.fullname}`",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            new_temp = generator.newTemp()
            label1 = generator.newLabel()
            label2 = generator.newLabel()
            label3 = generator.newLabel()
            generator.addIf(right_op.value, "0", "==", label1)
            generator.addGoto(label2)
            generator.addLabel(label1)
            generator.addCall("mathError")
            generator.addAssignation(new_temp, "0")
            generator.addGoto(label3)
            generator.addLabel(label2)
            generator.addExpression("P", "P", str(scope.size), "+")
            t1 = generator.newTemp()
            generator.addExpression(t1, "P", "1", "+")
            generator.addSetStack(t1, left_op.value)
            t2 = generator.newTemp()
            generator.addExpression(t2, "P", "2", "+")
            generator.addSetStack(t2, right_op.value)
            generator.addCall("module")
            generator.addGetStack(new_temp, "P")
            # if dominant_type == Type.I64 or dominant_type == Type.Int:
            #     generator.addExpression(
            #         new_temp, "(int)" + left_op.value, right_op.value, self.operator
            #     )
            # else:
            #     generator.addExpression(
            #         new_temp, left_op.value, right_op.value, self.operator
            #     )
            generator.addLabel(label3)
            generator.addExpression("P", "P", str(scope.size), "-")
            return Value(new_temp, True, dominant_type, "", "")
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

            if (left_op.type == Type.Str or left_op.type == Type.String) or (
                right_op.type == Type.Str or right_op.type == Type.String
            ):
                generator.addExpression("P", "P", str(scope.size), "+")
                t1 = generator.newTemp()
                t2 = generator.newTemp()
                t3 = generator.newTemp()
                generator.addExpression(t1, "P", "1", "+")
                generator.addSetStack(t1, left_op.value)
                generator.addExpression(t2, "P", "2", "+")
                generator.addSetStack(t2, right_op.value)
                generator.addCall("compareStrings")
                generator.addGetStack(t3, "P")
                generator.addExpression("P", "P", str(scope.size), "-")
                generator.addIf(t3, "1", "==", true_label)
                generator.addGoto(false_label)
            else:
                generator.addIf(
                    left_op.value, right_op.value, self.operator, true_label
                )
                generator.addGoto(false_label)

            return Value("", False, Type.Bool, [true_label], [false_label])

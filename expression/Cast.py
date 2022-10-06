from util.Error import Error, ERRORS_
from util.Expression import Expression
from util.Scope import Scope
from util.Generator import Generator
from util.Symbol import Value
from util.Types import Type


class Cast(Expression):
    def __init__(self, line: int, column: int, expr: Expression, type: Type) -> None:
        super().__init__(line, column)
        self.expr = expr
        self.type = type

    def execute(self, scope: Scope, generator: Generator) -> Value:
        expr = self.expr.execute(scope, generator)
        if self.type == Type.I64 or self.type == Type.Usize:
            if expr.getType() == Type.Str or expr.getType() == Type.String:
                err = Error(
                    self.line,
                    self.column,
                    f"Castear `{expr.type.fullname}` a `{self.type.fullname}` es  inválido",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            return Value(f"(int){expr.value}", expr.isTemp(), self.type, [""], [""])
        elif self.type == Type.F64:
            if expr.getType() == Type.Str or expr.getType() == Type.String:
                err = Error(
                    self.line,
                    self.column,
                    f"Castear `{expr.type.fullname}` a `{self.type.fullname}` es  inválido",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            return Value(f"(float){expr.value}", expr.isTemp(), self.type, [""], [""])
        elif self.type == Type.Bool:
            if expr.getType() != Type.Bool:
                err = Error(
                    self.line,
                    self.column,
                    "No se puede castear a `bool`",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            return expr
        elif self.type == Type.Str:
            err = Error(
                self.line,
                self.column,
                f"Casteo no-primitivo: `{expr.getType().fullname}` como `&str`",
                scope.name,
            )
            ERRORS_.append(err)
        elif self.type == Type.String:
            err = Error(
                self.line,
                self.column,
                f"Casteo no-primitivo: `{expr.getType().fullname}` como `String`",
                scope.name,
            )
            ERRORS_.append(err)
        elif self.type == Type.Char:
            if (
                expr.getType() == Type.I64
                or expr.getType() == Type.Usize
                or expr.getType() == Type.Int
            ):
                return Value(
                    f"(char){expr.value}", expr.isTemp(), self.type, [""], [""]
                )
            err = Error(
                self.line,
                self.column,
                "No se puede castear a `bool`",
                scope.name,
            )
            ERRORS_.append(err)
            return
        else:
            err = Error(
                self.line,
                self.column,
                f"Casteo no permitido: `{expr.getType().fullname}` como `{self.type.fullname}`",
                scope.name,
            )
            ERRORS_.append(err)
            return

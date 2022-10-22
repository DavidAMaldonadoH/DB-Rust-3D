from util.Expression import Expression
from util.Generator import Generator
from util.Symbol import Value
from util.Types import Type
from util.Scope import Scope
from util.Error import ERRORS_, Error


class Len(Expression):
    def __init__(self, line: int, column: int, expr: Expression):
        super().__init__(line, column)
        self.expr = expr

    def execute(self, scope: Scope, generator: Generator) -> Value:
        val = self.expr.execute(scope, generator)
        if isinstance(val.type, dict):
            return Value(str(val.type["size"]), False, Type.Usize, [], [])
        else:
            err = Error(
                self.line,
                self.column,
                "Se esperaba un arreglo o vector, pero se obtuvo un "
                + val.getType().fullname,
                scope.name,
            )
            ERRORS_.append(err)
            return

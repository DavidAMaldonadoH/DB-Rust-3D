from typing import Optional
from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Scope import Scope
from util.Symbol import Value


class CreateArray(Expression):
    def __init__(
        self,
        line: int,
        column: int,
        expressions: Optional[list[Expression]],
        expression: Optional[Expression],
        size: Optional[int],
    ):
        super().__init__(line, column)
        self.expressions = expressions
        self.expression = expression
        self.size = size

    def execute(self, scope: Scope, generator: Generator) -> Value:
        if self.expressions is not None:
            _values = []
            for expression in self.expressions:
                _values.append(expression.execute(scope, generator))
            if any(_value.type != _values[0].type for _value in _values):
                err = Error(
                    self.line, self.column, "Valores de diferente tipo", scope.name
                )
                ERRORS_.append(err)
                return
            if isinstance(_values[0].type, dict):
                return Value(
                    _values[0].value,
                    _values[0].is_temp,
                    {"type": _values[0].type, "size": len(_values)},
                    [],
                    [],
                )
            else:
                new_temp = generator.newTemp()
                generator.addComment("===================")
                generator.addComment2("Inicio Array")
                generator.addAssignation(new_temp, "H")
                for _value in _values:
                    generator.addSetHeap("H", _value.value)
                    generator.addExpression("H", "H", "1", "+")
                generator.addComment2("Final Array")
                generator.addComment("===================")
                return Value(
                    new_temp,
                    True,
                    {"type": _values[0].type, "size": len(_values)},
                    [],
                    [],
                )
        else:
            _value = self.expression.execute(scope, generator)
            if isinstance(_value.type, dict):
                return Value(
                    _values[0].value,
                    _values[0].is_temp,
                    {"type": _values[0].type, "size": len(_values)},
                    [],
                    [],
                )
            else:
                new_temp = generator.newTemp()
                generator.addComment("===================")
                generator.addComment2("Inicio Array")
                generator.addAssignation(new_temp, "H")
                for _ in range(self.size):
                    generator.addSetHeap("H", _value.value)
                    generator.addExpression("H", "H", "1", "+")
                generator.addComment2("Final Array")
                generator.addComment("===================")
                return Value(
                    new_temp,
                    True,
                    {"type": _value.type, "size": self.size},
                    [],
                    [],
                )

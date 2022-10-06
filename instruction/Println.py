import re
from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Instruction import Instruction
from util.Types import Type
from util.Symbol import Value
from util.Scope import Scope


class Println(Instruction):
    def __init__(self, line: int, column: int, values: list[Expression]):
        super().__init__(line, column)
        self.values = values

    def execute(self, scope: Scope, generator: Generator) -> any:
        _values: list[Value] = []
        for value in self.values:
            _values.append(value.execute(scope, generator))
        if len(_values) == 1:
            if _values[0].getType() != Type.Str:
                err = Error(
                    self.line,
                    self.column,
                    "El argumento de formato debe ser una cadena de formato",
                    scope.name,
                )
                ERRORS_.append(err)
            new_temp = generator.newTemp()
            generator.addExpression(new_temp, "P", "1", "+")
            generator.addSetStack(new_temp, _values[0].getValue())
            generator.addCall("imprimir")
            generator.addPrintf("c", "10")
            generator.addPrintf("c", "13")

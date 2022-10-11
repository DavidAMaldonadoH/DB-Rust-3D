from util.Error import ERRORS_, Error
from util.Types import Type
from util.Expression import Expression
from util.Instruction import Instruction
from util.Scope import Scope
from util.Generator import Generator
from util.Symbol import Value


class FunctionCall(Instruction):
    def __init__(self, line: int, column: int, name: str, args: list[Expression]):
        super().__init__(line, column)
        self.name = name
        self.args = args

    def execute(self, scope: Scope, generator: Generator) -> any:
        fn = scope.getFunction(self.name)
        if fn is None:
            err = Error(
                self.line,
                self.column,
                f"La funcion {self.name} no existe",
                scope.name,
            )
            ERRORS_.append(err)
            return
        if len(fn.parameters) != len(self.args):
            err = Error(
                self.line,
                self.column,
                f"La funcion {self.name} recibe {len(fn.parameters)} parametros",
                scope.name,
            )
            ERRORS_.append(err)
            return
        values = []
        for param, arg in zip(fn.parameters, self.args):
            val = arg["value"].execute(scope, generator)
            values.append(val)
            if val.type == Type.Int and (
                param["type"] == Type.I64 or param["type"] == Type.Usize
            ):
                val.type = param["type"]
            if param["type"] != val.type:
                err = Error(
                    self.line,
                    self.column,
                    f"El parametro {param['name']} de la funcion {self.name} es de tipo {param['type'].fullname} y se le esta pasando un valor de tipo {val.type.fullname}",
                    scope.name,
                )
                ERRORS_.append(err)
                return
        generator.addExpression("P", "P", str(scope.size), "+")
        for i, value in enumerate(values):
            new_temp = generator.newTemp()
            generator.addExpression(new_temp, "P", str(i + 1), "+")
            generator.addSetStack(new_temp, value.value)
        generator.addCall(fn.id)
        if fn.type != Type.Void:
            new_temp = generator.newTemp()
            generator.addGetStack(new_temp, "P")
            generator.addExpression("P", "P", str(scope.size), "-")
            return Value(new_temp, True, fn.type, [], [])
        generator.addExpression("P", "P", str(scope.size), "-")

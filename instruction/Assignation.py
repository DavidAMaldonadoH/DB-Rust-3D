from util.Expression import Expression
from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope
from util.Error import Error, ERRORS_
from util.Types import Type


class Assignation(Instruction):
    def __init__(self, line: int, column: int, id: str, value: Expression):
        super().__init__(line, column)
        self.id = id
        self.value = value

    def execute(self, scope: Scope, generator: Generator) -> any:
        var = scope.getVariable(self.id)
        if var is None:
            err = Error(
                self.line,
                self.column,
                f"La variable {self.id} no se ha declarado anteriormente.",
                scope.name,
            )
            ERRORS_.append(err)
            return
        if not var.isMutable():
            err = Error(
                self.line,
                self.column,
                f"{self.id} no es una variable mutable, no se puede modificar.",
                scope.name,
            )
            ERRORS_.append(err)
            return
        value_ = self.value.execute(scope, generator)
        var_type = var.getType()
        value_type = value_.getType()
        if value_type == Type.Int and (var_type == Type.I64 or var_type == Type.Usize):
            value_type = var_type
        if var_type != value_type:
            err = Error(
                self.line,
                self.column,
                f"Los tipos no coinciden: se esperaba {var.type.fullname} y se recibio {value_.getType().fullname}",
                scope.name,
            )
            ERRORS_.append(err)
            return
        generator.addSetStack(var.getPosition(), value_.getValue())

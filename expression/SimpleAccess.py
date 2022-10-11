from util.Error import Error, ERRORS_
from util.Expression import Expression
from util.Scope import Scope
from util.Generator import Generator
from util.Symbol import Value
from util.Types import Type


class SimpleAccess(Expression):
    def __init__(self, line: int, column: int, id: str) -> None:
        super().__init__(line, column)
        self.id = id

    def execute(self, scope: Scope, generator: Generator) -> Value:
        var = scope.getVariable(self.id)
        if var == None:
            err = Error(
                self.line,
                self.column,
                f"La variable {self.id} no existe en el ambito {scope.name}",
                scope.name,
            )
            ERRORS_.append(err)
            return
        t1 = generator.newTemp()
        generator.addExpression(t1, "P", str(var.position), "+")
        new_temp = generator.newTemp()
        generator.addGetStack(new_temp, t1)
        if var.type == Type.Bool:
            true_label = generator.newLabel()
            false_label = generator.newLabel()
            generator.addIf(new_temp, "1", "==", true_label)
            generator.addGoto(false_label)
            return Value(
                "",
                False,
                Type.Bool,
                [true_label],
                [false_label],
            )
        return Value(new_temp, True, var.type, [""], [""])

from util.Instruction import Instruction
from util.Expression import Expression
from util.Generator import Generator
from util.Types import Type
from util.Scope import Scope
from util.Error import ERRORS_, Error
from util.Symbol import Value


class NestedAssignation(Instruction):
    def __init__(self, line: int, column: int, vars: list, value: Expression):
        super().__init__(line, column)
        self.var = vars[0]
        self.indices = vars[1:]
        self.value = value

    def execute(self, scope: Scope, generator: Generator) -> any:
        actual_var = scope.getVariable(self.var)
        if actual_var is None:
            err = Error(
                self.line,
                self.column,
                "La variable con nombre " + self.var + " no existe",
                scope.name,
            )
            ERRORS_.append(err)
            return
        if not actual_var.isMutable():
            err = Error(
                self.line,
                self.column,
                "La variable con nombre " + self.var + " no es mutable",
                scope.name,
            )
            ERRORS_.append(err)
            return
        _value = self.value.execute(scope, generator)
        if actual_var.type2 == "Arreglo":
            label1 = generator.newLabel()
            label2 = generator.newLabel()
            aux = "0"
            for i, ind in enumerate(self.indices):
                index = ind.execute(scope, generator)
                if index.getType() == Type.Int or index.getType() == Type.Usize:
                    generator.addIf(index.value, "0", "<", label1)
                    generator.addIf(
                        index.value, str(actual_var.dimensions[i]), ">=", label1
                    )
                    t1 = generator.newTemp()
                    generator.addExpression(t1, aux, str(actual_var.dimensions[i]), "*")
                    t2 = generator.newTemp()
                    generator.addExpression(t2, t1, index.value, "+")
                    aux = t2
                else:
                    err = Error(
                        self.line,
                        self.column,
                        f"El índice debe ser de tipo `int` o `usize` no de tipo `{index.getType()}`",
                        scope.name,
                    )
                    ERRORS_.append(err)
                    return
            t1 = generator.newTemp()
            t3 = generator.newTemp()
            generator.addExpression(t3, "P", str(actual_var.position), "+")
            generator.addGetStack(t1, t3)
            t2 = generator.newTemp()
            generator.addExpression(t2, t1, aux, "+")
            if isinstance(_value.getType(), dict):
                self.setArray(scope, generator, t2, _value, _value.getType())
            else:
                generator.addSetHeap(t2, _value.value)
            generator.addGoto(label2)
            generator.addLabel(label1)
            generator.addCall("outOfBounds")
            generator.addLabel(label2)

    def setArray(
        self, scope: Scope, generator: Generator, pos: str, value: Value, type: any
    ):
        if isinstance(type.get("type"), dict):
            for _ in range(type["size"]):
                self.setArray(scope, generator, pos, value, type.get("type"))
        else:
            t1 = generator.newTemp()
            for _ in range(type["size"]):

                generator.addGetHeap(t1, value.value)
                generator.addSetHeap(pos, t1)
                generator.addExpression(pos, pos, "1", "+")
                generator.addExpression(value.value, value.value, "1", "+")

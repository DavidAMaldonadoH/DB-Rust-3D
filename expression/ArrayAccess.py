from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Symbol import Value
from util.Types import Type
from util.Scope import Scope


class ArrayAccess(Expression):
    def __init__(self, line: int, column: int, values: list[Expression]):
        super().__init__(line, column)
        self.array = values[0]
        self.indices = values[1:]

    def execute(self, scope: Scope, generator: Generator) -> Value:
        var = scope.getVariable(self.array)
        if var is None:
            err = Error(
                self.line,
                self.column,
                "La variable con nombre " + self.array + " no existe",
                scope.name,
            )
            ERRORS_.append(err)
            return
        if var.type2 == "Arreglo":
            label1 = generator.newLabel()
            label2 = generator.newLabel()
            aux = "0"
            for i, ind in enumerate(self.indices):
                index = ind.execute(scope, generator)
                if index.getType() == Type.Int or index.getType() == Type.Usize:
                    generator.addIf(index.value, "0", "<", label1)
                    generator.addIf(index.value, str(var.dimensions[i]), ">=", label1)
                    t1 = generator.newTemp()
                    generator.addExpression(t1, aux, str(var.dimensions[i]), "*")
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
            t4 = generator.newTemp()
            generator.addExpression(t4, "P", str(var.position), "+")
            generator.addGetStack(t1, t4)
            t2 = generator.newTemp()
            generator.addExpression(t2, t1, aux, "+")
            t3 = generator.newTemp()
            generator.addGetHeap(t3, t2)
            generator.addGoto(label2)
            generator.addLabel(label1)
            generator.addAssignation(t3, "0")
            generator.addCall("outOfBounds")
            generator.addLabel(label2)
            if len(self.indices) == len(var.dimensions):
                return Value(t3, True, var.type, [], [])
            else:
                generator.addExpression(t2, t2, t1, "-")
                array_type = {}
                for i in range(len(var.dimensions) - 1, len(self.indices) - 1, -1):
                    generator.addExpression(t2, t2, str(var.dimensions[i]), "*")
                    if i == len(var.dimensions) - 1:
                        array_type = {"size": var.dimensions[i], "type": var.type}
                    else:
                        array_type = {"size": var.dimensions[i], "type": array_type}
                generator.addExpression(t2, t2, t1, "+")
                return Value(t2, False, array_type, [], [])
        err = Error(
            self.line,
            self.column,
            f"El acceso por índice solo se puede hacer a un arreglo o vector no de tipo `{var.getType()}`",
            scope.name,
        )
        ERRORS_.append(err)
        return

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

    def getNestedSize(self, type: dict, arr: list):
        if isinstance(type["type"], dict):
            arr.append(type["size"])
            self.getNestedSize(type["type"], arr)
        else:
            arr.append(type["size"])

    def execute(self, scope: Scope, generator: Generator) -> any:
        if len(self.values) == 1:
            format_str = self.values[0].execute(scope, generator)
            if format_str.getType() != Type.Str:
                err = Error(
                    self.line,
                    self.column,
                    "El argumento de formato debe ser una cadena de formato",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            self.printStr(scope, generator, format_str)
            generator.addPrintf("c", "10")
            generator.addPrintf("c", "13")
        else:
            format_str = self.values[0].execute(scope, generator)
            if format_str.getType() != Type.Str:
                err = Error(
                    self.line,
                    self.column,
                    "El argumento de formato debe ser una cadena de formato",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            isNone: bool = False
            fields = re.split(r"{}|{\:\?}", format_str.getValue())
            for i, field in enumerate(fields):
                if i != len(fields) - 1:
                    if field != "":
                        new_temp = generator.newTemp()
                        generator.addComment("===================")
                        generator.addComment2("Inicio Str")
                        generator.addAssignation(new_temp, "H")
                        format_str = new_temp
                        for char in field:
                            generator.addSetHeap("H", str(ord(char)))
                            generator.addExpression("H", "H", "1", "+")
                        generator.addSetHeap("H", "-1")
                        generator.addExpression("H", "H", "1", "+")
                        generator.addComment2("Final Str")
                        generator.addComment("===================")
                        self.printStr(
                            scope, generator, Value(format_str, True, Type.Str, [], [])
                        )
                    value = self.values[i + 1].execute(scope, generator)
                    if value is None:
                        isNone = True
                        break
                    if isinstance(value.type, dict):
                        self.printLists(scope, generator, value, value.type)
                    else:
                        self.printPrimitive(scope, generator, value)
                else:
                    if field != "":
                        new_temp = generator.newTemp()
                        generator.addComment("===================")
                        generator.addComment2("Inicio Str")
                        generator.addAssignation(new_temp, "H")
                        format_str = new_temp
                        for char in field:
                            generator.addSetHeap("H", str(ord(char)))
                            generator.addExpression("H", "H", "1", "+")
                        generator.addSetHeap("H", "-1")
                        generator.addExpression("H", "H", "1", "+")
                        generator.addComment2("Final Str")
                        generator.addComment("===================")
                        self.printStr(
                            scope, generator, Value(format_str, True, Type.Str, [], [])
                        )
            if isNone:
                err = Error(
                    self.line,
                    self.column,
                    "El valor recibido no se puede imprimir",
                    scope.name,
                )
                ERRORS_.append(err)
                return
            generator.addPrintf("c", "10")
            generator.addPrintf("c", "13")

    def printStr(self, scope: Scope, generator: Generator, value: Value):
        generator.addExpression("P", "P", str(scope.size), "+")
        new_temp = generator.newTemp()
        generator.addExpression(new_temp, "P", "1", "+")
        generator.addSetStack(new_temp, value.getValue())
        generator.addCall("imprimir")
        generator.addExpression("P", "P", str(scope.size), "-")

    def printPrimitive(self, scope: Scope, generator: Generator, value: Value):
        if value.getType() == Type.I64 or value.getType() == Type.Int:
            generator.addPrintf("d", "(int)" + value.getValue())
        elif value.getType() == Type.F64:
            generator.addPrintf("f", value.getValue())
        elif value.getType() == Type.Char:
            generator.addPrintf("c", "(int)" + value.getValue())
        elif value.getType() == Type.Usize:
            generator.addPrintf("d", "(int)" + value.getValue())
        elif value.getType() == Type.Bool:
            new_label = generator.newLabel()
            for label in value.true_label:
                generator.addLabel(label)
            generator.addCall("printTrue")
            generator.addGoto(new_label)
            for label in value.false_label:
                generator.addLabel(label)
            generator.addCall("printFalse")
            generator.addLabel(new_label)
        elif value.getType() == Type.Str or value.getType() == Type.String:
            self.printStr(scope, generator, value)
        else:
            err = Error(
                self.line,
                self.column,
                "No se puede imprimir el tipo de dato",
                scope.name,
            )
            ERRORS_.append(err)
            return

    def printLists(self, scope: Scope, generator: Generator, value: Value, type: any):
        if isinstance(type.get("type"), dict):
            generator.addPrintf("c", str(ord("[")))
            for i in range(type["size"]):
                self.printLists(scope, generator, value, type["type"])
                if i != type["size"] - 1:
                    generator.addPrintf("c", str(ord(",")))
            generator.addPrintf("c", str(ord("]")))
        else:
            new_temp = generator.newTemp()
            generator.addPrintf("c", str(ord("[")))
            for i in range(type["size"]):
                generator.addGetHeap(new_temp, value.value)
                val = Value(
                    new_temp, True, type["type"], value.true_label, value.false_label
                )
                if i != type["size"] - 1:
                    self.printPrimitive(scope, generator, val)
                    generator.addPrintf("c", str(ord(",")))
                else:
                    self.printPrimitive(scope, generator, val)
                generator.addExpression(value.value, value.value, "1", "+")
            generator.addPrintf("c", str(ord("]")))

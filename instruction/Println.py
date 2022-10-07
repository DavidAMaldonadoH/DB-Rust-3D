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
            self.printStr(generator, format_str)
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
            fields = re.split(r"{}|{\:\?}", format_str.getValue())
            for i, field in enumerate(fields):
                if i != len(fields) - 1:
                    if field != "":
                        new_temp = generator.newTemp()
                        generator.addComment("===================")
                        generator.addComment2("Inicio Str")
                        generator.addAsignation(new_temp, "H")
                        format_str = new_temp
                        for char in field:
                            generator.addSetHeap("H", str(ord(char)))
                            generator.addExpression("H", "H", "1", "+")
                        generator.addSetHeap("H", "-1")
                        generator.addExpression("H", "H", "1", "+")
                        generator.addComment2("Final Str")
                        generator.addComment("===================")
                        self.printStr(
                            generator, Value(format_str, True, Type.Str, [], [])
                        )
                    value = self.values[i + 1].execute(scope, generator)
                    self.printPrimitive(scope, generator, value)
                else:
                    if field != "":
                        new_temp = generator.newTemp()
                        generator.addComment("===================")
                        generator.addComment2("Inicio Str")
                        generator.addAsignation(new_temp, "H")
                        format_str = new_temp
                        for char in field:
                            generator.addSetHeap("H", str(ord(char)))
                            generator.addExpression("H", "H", "1", "+")
                        generator.addSetHeap("H", "-1")
                        generator.addExpression("H", "H", "1", "+")
                        generator.addComment2("Final Str")
                        generator.addComment("===================")
                        self.printStr(
                            generator, Value(format_str, True, Type.Str, [], [])
                        )
            generator.addPrintf("c", "10")
            generator.addPrintf("c", "13")

    def printStr(self, generator: Generator, value: Value):
        new_temp = generator.newTemp()
        generator.addExpression(new_temp, "P", "1", "+")
        generator.addSetStack(new_temp, value.getValue())
        generator.addCall("imprimir")

    def printPrimitive(self, scope: Scope, generator: Generator, value: Value):
        if value.getType() == Type.I64:
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
            self.printStr(generator, value)
        else:
            err = Error(
                self.line,
                self.column,
                "No se puede imprimir el tipo de dato",
                scope.name,
            )
            ERRORS_.append(err)
            return

import re
from util.Expression import Expression
from util.Generator import Generator
from util.Scope import Scope
from util.Symbol import Value
from util.Types import Type


class Literal(Expression):
    def __init__(self, line: int, column: int, value: any) -> None:
        super().__init__(line, column)
        self.value = value

    def execute(self, scope: Scope, generator: Generator):
        type: Type
        value: str
        if isinstance(self.value, bool):
            true_label = generator.newLabel()
            false_label = generator.newLabel()
            type = Type.Bool
            if self.value:
                generator.addGoto(true_label)
            else:
                generator.addGoto(false_label)
            return Value("", False, type, [true_label], [false_label])
        elif isinstance(self.value, int):
            type = Type.Int
            value = str(self.value)
        elif isinstance(self.value, float):
            type = Type.F64
            value = str(self.value)
        elif isinstance(self.value, str):
            if re.match(r"\'((\\)?(.{1}?))\'", self.value):
                type = Type.Char
                value = str(ord(self.value[1]))
            else:
                if "{}" in self.value or "{:?}" in self.value:
                    return Value(self.value, False, Type.Str, [], [])
                type = Type.Str
                new_temp = generator.newTemp()
                generator.addComment("===================")
                generator.addComment2("Inicio Str")
                generator.addAssignation(new_temp, "H")
                value = new_temp
                for char in self.value:
                    generator.addSetHeap("H", str(ord(char)))
                    generator.addExpression("H", "H", "1", "+")
                generator.addSetHeap("H", "-1")
                generator.addExpression("H", "H", "1", "+")
                generator.addComment2("Final Str")
                generator.addComment("===================")
        return Value(value, False, type, [], [])

from typing import Optional
from instruction.Declaration import Declaration
from util.Generator import Generator
from util.Instruction import Instruction
from util.Expression import Expression
from util.Error import ERRORS_, Error
from util.Types import Type
from util.Scope import Scope


class For(Instruction):
    def __init__(
        self,
        line: int,
        column: int,
        id: str,
        start: Expression,
        end: Optional[Expression],
        code: Instruction,
    ):
        super().__init__(line, column)
        self.id = id
        self.start = start
        self.end = end
        self.code = code

    def execute(self, scope: Scope, generator: Generator) -> any:
        if self.end != None:
            label_start = generator.newLabel()
            label_end = generator.newLabel()
            generator.display.nextPtr()
            generator.getDisplayPtr().inicio = label_start
            generator.getDisplayPtr().salida = label_end

            new_temp = generator.newTemp()
            new_temp2 = generator.newTemp()
            end = self.end.execute(scope, generator)
            declaration = Declaration(
                self.line, self.column, True, self.id, end.type, self.start
            )
            declaration.execute(scope, generator)
            var = scope.getVariable(self.id)
            generator.addAssignation(new_temp, "1")
            generator.addGetStack(new_temp2, str(var.getPosition()))
            generator.addLabel(label_start)
            generator.addIf(new_temp2, end.value, "==", label_end)
            self.code.execute(scope, generator)
            generator.addExpression(new_temp2, new_temp2, new_temp, "+")
            generator.addSetStack(str(var.getPosition()), new_temp2)
            generator.addGoto(label_start)
            generator.addLabel(label_end)
            generator.display.prevPtr()

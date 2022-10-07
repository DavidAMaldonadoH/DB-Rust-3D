from util.Error import ERRORS_, Error
from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope


class Loop(Instruction):
    def __init__(self, line: int, column: int, code: Instruction):
        super().__init__(line, column)
        self.code = code

    def execute(self, scope: Scope, generator: Generator) -> any:
        self.code.setName("Loop")
        label_inicio = generator.newLabel()
        generator.addLabel(label_inicio)
        generator.display.nextPtr()
        generator.getDisplayPtr().salida = generator.newLabel()
        generator.getDisplayPtr().inicio = label_inicio
        generator.getDisplayPtr().contB = 0
        self.code.execute(scope, generator)
        generator.addGoto(label_inicio)
        generator.addLabel(generator.getDisplayPtr().salida)
        if generator.getDisplayPtr().contB == 0:
            err = Error(
                self.line,
                self.column,
                "Ciclo loop sin `break`!",
                scope.name,
            )
            ERRORS_.append(err)
            return
        generator.display.prevPtr()

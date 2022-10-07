from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Instruction import Instruction
from util.Types import Type
from util.Scope import Scope


class While(Instruction):
    def __init__(self, line: int, column: int, expr: Expression, code: Instruction):
        super().__init__(line, column)
        self.expr = expr
        self.code = code

    def execute(self, scope: Scope, generator: Generator) -> any:
        self.code.setName("While")
        label_inicio = generator.newLabel()
        generator.addLabel(label_inicio)
        cond = self.expr.execute(scope, generator)
        if cond.type != Type.Bool:
            err = Error(
                self.line,
                self.column,
                f"Los tipos no coinciden: se experaba `bool`, se encontro {cond.getType().fullname}",
                scope.name,
            )
            ERRORS_.append(err)
            return
        generator.display.nextPtr()
        generator.getDisplayPtr().salida = cond.false_label[0]
        generator.getDisplayPtr().inicio = label_inicio
        for label in cond.true_label:
            generator.addLabel(label)
        self.code.execute(scope, generator)
        generator.addGoto(label_inicio)
        for label in cond.false_label:
            generator.addLabel(label)
        generator.display.prevPtr()

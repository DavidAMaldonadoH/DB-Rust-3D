from typing import Optional
from util.Error import ERRORS_, Error
from util.Expression import Expression
from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope
from util.Types import Type


class If(Instruction):
    def __init__(
        self,
        line: int,
        column: int,
        expr: Expression,
        code: Instruction,
        elsest: Optional[Instruction],
        label: str = "",
    ):
        super().__init__(line, column)
        self.expr = expr
        self.code = code
        self.elsest = elsest
        self.label = label

    def execute(self, scope: Scope, generator: Generator) -> any:
        self.code.setName("If")
        cond = self.expr.execute(scope, generator)
        if cond.getType() == Type.Bool:
            if self.label == "":
                label_salida = generator.newLabel()
            else:
                label_salida = self.label
            for label in cond.true_label:
                generator.addLabel(label)
            self.code.execute(scope, generator)
            generator.addGoto(label_salida)
            for label in cond.false_label:
                generator.addLabel(label)
            if self.elsest is not None:
                if isinstance(self.elsest, If):
                    self.elsest.label = label_salida
                self.elsest.execute(scope, generator)
            if self.label == "":
                generator.addLabel(label_salida)
        else:
            err = Error(
                self.line,
                self.column,
                f"Los tipos no coinciden: se experaba `bool`, se encontro {cond.getType().fullname}",
                scope.name,
            )
            ERRORS_.append(err)

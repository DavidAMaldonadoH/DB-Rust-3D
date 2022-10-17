from util.Error import Error, ERRORS_
from util.Generator import Generator
from util.Instruction import Instruction
from util.Expression import Expression
from util.Scope import Scope
from util.Symbol import Symbol, Value
from util.Types import Type


class Declaration(Instruction):
    def __init__(
        self,
        line: int,
        column: int,
        is_mutable: bool,
        id: str,
        type: any,
        value: Expression,
    ) -> None:
        super().__init__(line, column)
        self.is_mutable = is_mutable
        self.id = id
        self.type = type
        self.value = value

    def getNestedType(self, type: dict, arr: list):
        if isinstance(type["type"], dict):
            arr.append(type["size"])
            self.getNestedType(type["type"], arr)
        else:
            arr.append(type["size"])
            arr.append(type["type"])

    def execute(self, scope: Scope, generator: Generator) -> any:
        result: Value = self.value.execute(scope, generator)
        sizes_dec = []
        sizes_exp = []
        if isinstance(self.type, dict):
            self.getNestedType(self.type, sizes_dec)
            self.type = sizes_dec.pop()
            self.getNestedType(result.type, sizes_exp)
            result.type = sizes_exp.pop()
        if result.type == Type.Int and (
            self.type == Type.I64 or self.type == Type.Usize
        ):
            result.type = self.type
        if self.type != result.type:
            err = Error(
                self.line,
                self.column,
                f"Los tipos no coinciden: se esperaba {self.type.fullname} y se recibio {result.getType().fullname}",
                scope.name,
            )
            ERRORS_.append(err)
            return
        variable: Symbol
        if len(sizes_dec) > 0 and len(sizes_exp) > 0:
            if all(sizes_dec[i] == sizes_exp[i] for i in range(len(sizes_dec))):
                variable = scope.saveVariable(
                    self.id,
                    self.type,
                    "Arreglo",
                    self.is_mutable,
                    sizes_dec,
                    self.line,
                    self.column,
                )
        else:

            variable = scope.saveVariable(
                self.id,
                self.type,
                "Variable",
                self.is_mutable,
                [],
                self.line,
                self.column,
            )
        new_temp = generator.newTemp()
        generator.addExpression(new_temp, "P", str(variable.position), "+")
        if result.type == Type.Bool:
            new_label = generator.newLabel()
            for label in result.true_label:
                generator.addLabel(label)
            generator.addExpression(new_temp, "P", str(variable.position), "+")
            generator.addSetStack(new_temp, "1")
            generator.addGoto(new_label)
            for label in result.false_label:
                generator.addLabel(label)
            generator.addExpression(new_temp, "P", str(variable.position), "+")
            generator.addSetStack(new_temp, "0")
            generator.addLabel(new_label)
        else:
            generator.addSetStack(new_temp, result.value)
        # generator.addExpression("P", "P", "1", "+")
        return result.value

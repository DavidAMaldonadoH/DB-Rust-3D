from util.Generator import Generator
from util.Instruction import Instruction
from util.Scope import Scope
from util.Types import Type


class FunctionDeclaration(Instruction):
    def __init__(
        self,
        line: int,
        column: int,
        id: str,
        parameters: list,
        code: Instruction,
        type: Type,
        public: bool = False,
    ):
        super().__init__(line, column)
        self.id = id
        self.parameters = parameters
        self.code = code
        self.type = type
        self.public = public

    def execute(self, scope: Scope, generator: Generator) -> any:
        generator.code.append(f"{self.type.fullname} {self.id}() {{")
        self.code.execute(scope, generator)
        generator.code.append("return;")
        generator.code.append("}")

from util.Function import Function
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
        generator.code.append(f"void {self.id}() {{")
        self.code.name = self.id
        self.code.size = 1
        self.code.parameters = self.parameters
        self.code.execute(scope, generator)
        generator.code.append("return;")
        generator.code.append("}\n")
        fn = Function(self.id, self.parameters, self.type, self.public, self.code.size)
        scope.saveFunction(self.id, fn, self.line, self.column)

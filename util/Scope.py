from typing import Optional
from util.Error import Error, ERRORS_
from util.Function import Function
from util.Symbol import Symbol, SYMBOLS
from util.Types import Type


class Scope:
    def __init__(self, father: Optional["Scope"], name: str):
        self.father = father
        self.name = name
        self.size = 0 if father is None else father.size
        self.variables = dict()
        self.functions = dict()

    def getGlobal(self):
        while self.father != None:
            self = self.father
        return self

    def getVariable(self, name: str) -> Symbol:
        while True:
            if name in self.variables:
                return self.variables[name]
            if self.father == None:
                break
            self = self.father
        return None

    def saveVariable(
        self, name: str, type: Type, mutable: bool, line: int, col: int
    ) -> Symbol:
        if name in self.variables:
            err = Error(
                line,
                col,
                f"La variable {name} ya existe en el ambito {self.name}",
                self.name,
            )
            ERRORS_.append(err)
            return self.variables[name]
        self.variables[name] = Symbol(name, type, self.size, mutable)
        SYMBOLS.append(
            {
                "name": name,
                "type": "Variable",
                "type2": type.fullname,
                "scope": self.name,
                "position": self.size,
                "params": "",
                "size": "1",
            }
        )
        self.size += 1
        return self.variables[name]

    def getFunction(self, name: str) -> Function:
        while True:
            if name in self.functions:
                return self.functions[name]
            if self.father == None:
                break
            self = self.father
        return None

    def saveFunction(self, id: str, fn: Function, line: int, col: int):
        if id in self.functions:
            err = Error(
                line,
                col,
                f"La función {id} ya existe.",
                self.name,
            )
            ERRORS_.append(err)
        self.functions[id] = fn
        SYMBOLS.append(
            {
                "name": id,
                "type": "Funcion",
                "type2": fn.type.fullname,
                "scope": self.name,
                "position": "-1",
                "params": ",".join([p["name"] for p in fn.parameters]),
                "size": str(fn.size),
            }
        )
        SYMBOLS.append(
            {
                "name": "return",
                "type": "Variable",
                "type2": fn.type.fullname,
                "scope": fn.id,
                "position": "0",
                "params": "",
                "size": "1",
            }
        )

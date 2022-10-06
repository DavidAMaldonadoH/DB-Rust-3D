class Generator:
    def __init__(self) -> None:
        self.temporal = 0
        self.label = 0
        self.code = list()
        self.temps = list()

    def getCode(self) -> list[str]:
        return self.code

    def getTemps(self) -> list[str]:
        return self.temps

    def newTemp(self) -> str:
        temp = f"t{self.temporal}"
        self.temporal += 1
        self.temps.append(temp)
        return temp

    def newLabel(self) -> str:
        label = self.label
        self.label += 1
        return f"L{label}"

    def addLabel(self, label: str) -> None:
        self.code.append(f"{label}:")

    def addIf(self, left: str, right: str, operator: str, label: str) -> None:
        self.code.append(f"if ({left} {operator} {right}) goto {label};")

    def addGoto(self, label: str) -> None:
        self.code.append(f"goto {label};")

    def addExpression(self, target: str, left: str, right: str, operator: str) -> None:
        self.code.append(f"{target} = {left} {operator} {right};")

    def addAsignation(self, target: str, value: str) -> None:
        self.code.append(f"{target} = {value};")

    def addPrintf(self, typePrint: str, value: str) -> None:
        self.code.append(f'printf("%{typePrint}", {value});')

    def addSetStack(self, index: str, value: str) -> None:
        self.code.append(f"stack[(int){index}] = {value};")

    def addGetStack(self, target: str, index: str) -> None:
        self.code.append(f"{target} = stack[(int){index}];")

    def addSetHeap(self, index: str, value: str) -> None:
        self.code.append(f"heap[(int){index}] = {value};")

    def addGetHeap(self, target: str, index: str) -> None:
        self.code.append(f"{target} = heap[(int){index}];")

    def addComment(self, content: str) -> None:
        self.code.append(f"//{content}")

    def addComment2(self, content: str) -> None:
        self.code.append(f"/***{content}***/")

    def addCall(self, name: str) -> None:
        self.code.append(f"{name}();")

    def addImprimir(self) -> None:
        self.code.append("void imprimir() {")
        t1 = self.newTemp()
        self.addExpression(t1, "P", "1", "+")
        t2 = self.newTemp()
        self.addGetStack(t2, t1)
        l1 = self.newLabel()
        self.addLabel(l1)
        t3 = self.newTemp()
        self.addGetHeap(t3, t2)
        l2 = self.newLabel()
        self.addIf(t3, "-1", "==", l2)
        self.addPrintf("c", f"(int){t3}")
        self.addExpression(t2, t2, "1", "+")
        self.addGoto(l1)
        self.addLabel(l2)
        self.code.append("return;")
        self.code.append("}")

from util.Display import Display


class Generator:
    def __init__(self) -> None:
        self.temporal = 0
        self.label = 0
        self.code = list()
        self.temps = list()
        self.display = Display()

    def getDisplayPtr(self) -> None:
        return self.display.content[self.display.display_ptr]

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
        self.code.append("}\n")

    def addPrintTrue(self) -> None:
        self.code.append("void printTrue() {")
        self.addPrintf("c", "116")
        self.addPrintf("c", "114")
        self.addPrintf("c", "117")
        self.addPrintf("c", "101")
        self.code.append("return;")
        self.code.append("}\n")

    def addPrintFalse(self) -> None:
        self.code.append("void printFalse() {")
        self.addPrintf("c", "102")
        self.addPrintf("c", "97")
        self.addPrintf("c", "108")
        self.addPrintf("c", "115")
        self.addPrintf("c", "101")
        self.code.append("return;")
        self.code.append("}\n")

    def addModule(self) -> None:
        self.code.append("void module() {")
        t1 = self.newTemp()
        self.addExpression(t1, "P", "1", "+")
        t2 = self.newTemp()
        self.addGetStack(t2, t1)
        t3 = self.newTemp()
        self.addExpression(t3, "P", "2", "+")
        t4 = self.newTemp()
        self.addGetStack(t4, t3)
        label1 = self.newLabel()
        self.addLabel(label1)
        label2 = self.newLabel()
        self.addIf(t2, "0", "<", label2)
        self.addExpression(t2, t2, t4, "-")
        self.addGoto(label1)
        self.addLabel(label2)
        self.addExpression(t2, t2, t4, "+")
        self.addSetStack("P", t2)
        self.code.append("return;")
        self.code.append("}\n")

    def addAbsolute(self):
        self.code.append("void absolute() {")
        t1 = self.newTemp()
        self.addExpression(t1, "P", "1", "+")
        t2 = self.newTemp()
        self.addGetStack(t2, t1)
        label1 = self.newLabel()
        label2 = self.newLabel()
        self.addIf(t2, "0", "<", label1)
        self.addGoto(label2)
        t3 = self.newTemp()
        self.addLabel(label1)
        self.addAsignation(t3, "-1")
        self.addExpression(t2, t2, t3, "*")
        self.addLabel(label2)
        self.addSetStack("P", t2)
        self.code.append("return;")
        self.code.append("}\n")

    def addSquareRoot(self):
        self.code.append("void squareRoot() {")
        t1 = self.newTemp()
        t2 = self.newTemp()
        t3 = self.newTemp()
        t4 = self.newTemp()
        t5 = self.newTemp()
        t6 = self.newTemp()
        t7 = self.newTemp()
        t8 = self.newTemp()
        t9 = self.newTemp()
        label1 = self.newLabel()
        label2 = self.newLabel()
        label3 = self.newLabel()
        self.addExpression(t1, "P", "1", "+")
        self.addGetStack(t2, t1)
        self.addAsignation(t4, "1")
        self.addExpression(t4, t4, "10000", "/")
        self.addExpression(t3, t2, "2", "/")
        self.addAsignation(t8, t3)
        self.addExpression(t5, t3, t3, "*")
        self.addExpression(t5, t5, t2, "-")
        self.addExpression(t6, "2", t3, "*")
        self.addLabel(label1)
        self.addExpression(t7, "0", t4, "-")
        self.addIf(t7, t5, ">=", label2)
        self.addIf(t5, t4, ">=", label2)
        self.addGoto(label3)
        self.addLabel(label2)
        self.addExpression(t9, t5, t6, "/")
        self.addExpression(t8, t8, t9, "-")
        self.addExpression(t5, t8, t8, "*")
        self.addExpression(t5, t5, t2, "-")
        self.addExpression(t6, "2", t3, "*")
        self.addGoto(label1)
        self.addLabel(label3)
        self.addSetStack("P", t8)
        self.code.append("return;")
        self.code.append("}\n")

    def addPower(self):
        self.code.append("void power() {")
        t1 = self.newTemp()
        t2 = self.newTemp()
        t3 = self.newTemp()
        t4 = self.newTemp()
        t5 = self.newTemp()
        label1 = self.newLabel()
        label2 = self.newLabel()
        self.addExpression(t1, "P", "1", "+")
        self.addGetStack(t2, t1)
        self.addExpression(t3, "P", "2", "+")
        self.addGetStack(t4, t3)
        self.addAsignation(t5, "1")
        self.addLabel(label1)
        self.addIf(t4, "0", "==", label2)
        self.addExpression(t5, t5, t2, "*")
        self.addExpression(t4, t4, "1", "-")
        self.addGoto(label1)
        self.addLabel(label2)
        self.addSetStack("P", t5)
        self.code.append("return;")
        self.code.append("}\n")

    def addMathError(self):
        self.code.append("void mathError() {")
        self.addPrintf("c", str(ord("M")))
        self.addPrintf("c", str(ord("a")))
        self.addPrintf("c", str(ord("t")))
        self.addPrintf("c", str(ord("h")))
        self.addPrintf("c", str(ord("E")))
        self.addPrintf("c", str(ord("r")))
        self.addPrintf("c", str(ord("r")))
        self.addPrintf("c", str(ord("o")))
        self.addPrintf("c", str(ord("r")))
        self.code.append("return;")
        self.code.append("}\n")

    def addConcatenate(self):
        self.code.append("void concatenate() {")
        new_temp = self.newTemp()
        self.addAsignation(new_temp, "H")
        t1 = self.newTemp()
        t2 = self.newTemp()
        t3 = self.newTemp()
        t4 = self.newTemp()
        t5 = self.newTemp()
        self.addExpression(t1, "P", "1", "+")
        self.addGetStack(t2, t1)
        self.addExpression(t3, "P", "2", "+")
        self.addGetStack(t4, t3)
        label1 = self.newLabel()
        label2 = self.newLabel()
        label3 = self.newLabel()
        self.addLabel(label1)
        self.addGetHeap(t5, t2)
        self.addIf(t5, "-1", "==", label2)
        self.addSetHeap("H", t5)
        self.addExpression("H", "H", "1", "+")
        self.addExpression(t2, t2, "1", "+")
        self.addGoto(label1)
        self.addLabel(label2)
        self.addGetHeap(t5, t4)
        self.addIf(t5, "-1", "==", label3)
        self.addSetHeap("H", t5)
        self.addExpression("H", "H", "1", "+")
        self.addExpression(t4, t4, "1", "+")
        self.addGoto(label2)
        self.addLabel(label3)
        self.addSetHeap("H", "-1")
        self.addExpression("H", "H", "1", "+")
        self.addSetStack("P", new_temp)
        self.code.append("return;")
        self.code.append("}\n")

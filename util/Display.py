class DisplayNode:
    def __init__(self) -> None:
        self.salida = ""
        self.inicio = ""
        self.contB = 0


class Display:
    def __init__(self) -> None:
        self.content: list[DisplayNode] = [DisplayNode() for _ in range(1000)]
        self.display_ptr = 0

    def nextPtr(self) -> None:
        self.display_ptr += 1

    def prevPtr(self) -> None:
        self.display_ptr -= 1

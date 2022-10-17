from util.Types import Type


class Symbol:
    def __init__(
        self,
        id: str,
        type: Type,
        type2: str,
        position: int,
        mutable: bool,
        dimensions: list[int],
    ) -> None:
        self.id = id
        self.type = type
        self.type2 = type2
        self.position = position
        self.mutable = mutable
        self.dimensions = dimensions

    def isMutable(self) -> bool:
        return self.mutable

    def getType(self) -> Type:
        return self.type

    def getType2(self) -> str:
        return self.type2

    def getPosition(self) -> int:
        return self.position

    def getDimensions(self) -> list[int]:
        return self.dimensions


SYMBOLS = []


class Value:
    def __init__(
        self,
        value: str,
        is_temp: bool,
        type: Type,
        true_label: list[str],
        false_label: list[str],
    ) -> None:
        self.value = value
        self.is_temp = is_temp
        self.type = type
        self.true_label = true_label
        self.false_label = false_label

    def getTrueLabels(self) -> str:
        label: str
        for i, lbl in enumerate(self.true_label):
            if i == len(self.true_label) - 1:
                label += lbl
                break
            label += lbl, ", "

    def getFalseLables(self) -> str:
        label: str
        for i, lbl in enumerate(self.false_label):
            if i == len(self.false_label) - 1:
                label += lbl
                break
            label += lbl, ", "

    def isTemp(self) -> bool:
        return self.is_temp

    def getType(self) -> Type:
        return self.type

    def getValue(self) -> str:
        return self.value

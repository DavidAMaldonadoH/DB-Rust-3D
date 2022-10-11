class Function:
    def __init__(
        self, id: str, parameters: list, type: any, public: bool, size: int
    ) -> None:
        self.id = id
        self.parameters = parameters
        self.type = type
        self.public = public
        self.size = size

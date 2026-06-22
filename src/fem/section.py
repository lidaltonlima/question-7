class Section:
    name: str  # None da seção
    A: float  # Area
    I: float  # Inércia  # noqa: E741

    def __init__(self, name: str, A: float, I: float) -> None:  # noqa: E741, N803
        self.name = name
        self.A = A
        self.I = I

    def __repr__(self) -> str:
        """Representação do objeto"""
        return f'{self.__class__.__name__}({self.name})'

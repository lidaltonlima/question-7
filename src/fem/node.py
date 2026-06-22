class Node:
    name: str  # Nome do nó
    x: float  # Nó inicial
    y: float  # Nó final

    def __init__(self, name: str, x: float, y: float) -> None:
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """Representação do objeto"""
        return f'{self.__class__.__name__}({self.name})'

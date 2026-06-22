class Material:
    name: str  # Nome do material
    E: float  # Módulo de elasticidade Longitudinal

    def __init__(self, name: str, E: float) -> None:  # noqa: N803
        self.name = name
        self.E = E

    def __repr__(self) -> str:
        """Representação do objeto"""
        return f'{self.__class__.__name__}({self.name})'

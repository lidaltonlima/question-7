from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


class Node:
    name: str  # Nome do nó
    x: float  # Nó inicial
    y: float  # Nó final
    coord: NDArray  # Posição do nó

    def __init__(self, name: str, x: float, y: float) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.coord = np.array([x, y])

    def __repr__(self) -> str:
        """Representação do objeto"""
        return f'{self.__class__.__name__}({self.name})'

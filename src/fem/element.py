from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .scripts import get_kl, get_node_distance, get_R

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from .load import ConstantLoad
    from .material import Material
    from .node import Node
    from .section import Section


class Element:
    name: str  # Nome do elemento
    node_i: Node  # Nó inicial
    node_f: Node  # Nó final
    material: Material  # Material
    section: Section  # Seção
    length: float  # Comprimento (L)
    R: NDArray  # Matriz de rotação
    kl: NDArray  # Matriz de rigidez local no sistema local
    kg: NDArray  # Matriz de rigidez local no sistema global
    fl: NDArray  # Vetor de forças local no sistema local
    fg: NDArray  # Vetor de forças local no sistema Global
    end_efforts: (
        NDArray | None
    )  # Cargas nos nós para o diagrama de corpo livre

    def __init__(
        self,
        name: str,
        node_i: Node,
        node_f: Node,
        material: Material,
        section: Section,
    ) -> None:
        self.name = name
        self.node_i = node_i
        self.node_f = node_f
        self.material = material
        self.section = section

        self.length = get_node_distance(node_i, node_f)
        self.R = get_R(self)
        self.kl = get_kl(self)
        self.kg = self.R.T @ self.kl @ self.R  # Transformação de base
        self.fl = np.zeros(6)
        self.fg = np.zeros(6)
        self.end_efforts = None

    def distribute_to_nodal(self, load: ConstantLoad) -> None:
        """Calcula a carga nodal equivalente devido a carga distribuída

        Args:
            load (ConstantLoad): A carga aplicada no elemento
        """
        L = self.length  # noqa: N806
        q = load.Fy

        Fyi = -(q * L) / 2  # noqa: N806
        Fyf = Fyi  # noqa: N806

        Mzi = -(q * L**2) / 12  # noqa: N806
        Mzf = -Mzi  # noqa: N806

        # A carga equivalente deve refletir apenas o load atual desta chamada.
        self.fl = np.array([0, Fyi, Mzi, 0, Fyf, Mzf])
        self.fg = self.R.T @ self.fl

    def __repr__(self) -> str:
        """Representação do objeto"""
        return f'{self.__class__.__name__}({self.name})'

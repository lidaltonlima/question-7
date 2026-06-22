from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from .scripts import get_F, get_K

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from .element import Element
    from .load import LoadCase
    from .node import Node
    from .support import Support


class Structure:
    nodes: list[Node]  # Nós
    elements: list[Element]  # Elementos
    load_cases: list[LoadCase]  # Casos de carga
    support: Support | None
    is_calculated: bool  # Controla se a estrutura já foi calculada
    K: NDArray | None  # Matriz de rigidez global
    F: NDArray | None  # Vetor de forças nodais global
    disp: NDArray | None  # Vetor de deslocamentos

    def __init__(self) -> None:
        self.nodes = []
        self.elements = []
        self.load_cases = []
        self.support = None
        self.is_calculated = False
        self.K = None
        self.F = None
        self.disp = None

    def add_node(self, node: Node) -> None:
        """Adiciona nós na estrutura.

        Args:
            node (Node): O nó a ser adicionado.
        """
        self.nodes.append(node)

    def add_element(self, element: Element) -> None:
        """Adiciona elementos na estrutura.

        Args:
            element (Element): O elemento a ser adicionado.
        """
        self.elements.append(element)

    def add_load_case(self, load_case: LoadCase) -> None:
        """Adiciona um caso de carga na estrutura.

        Args:
            load_case (LoadCase): O caso de carga a ser adicionado.
        """
        self.load_cases.append(load_case)

    def add_support(self, support: Support) -> None:
        """Adiciona as condições de contorno

        Args:
            support (Support): As condições de contorno
        """
        self.support = support

    def calculate(self) -> None:
        """Calcula a estrutura"""
        self.is_calculated = True

        # Pega a matriz de rigidez global
        self.F = get_F(self.nodes, self.elements, self.load_cases)
        self.K = get_K(self.nodes, self.elements)

        K_temp = self.K.copy()  # noqa: N806
        F_temp = self.F.copy()  # noqa: N806

        for node, support in self.support.nodal().items():
            # Onde começa o índice do nó
            index_Dx = self.nodes.index(node) * 3  # noqa: N806
            index_Dy = index_Dx + 1  # noqa: N806
            index_Rz = index_Dx + 2  # noqa: N806

            # Usa técnica dos zeros e uns
            if support.Dx:
                # Matriz de Rigidez
                K_temp[index_Dx, :] = 0  # Zera a linha
                K_temp[:, index_Dx] = 0  # Zera a coluna
                K_temp[index_Dx, index_Dx] = 1  # Coloca 1 da diagonal

                F_temp[index_Dx] = 0

            if support.Dy:
                K_temp[index_Dy, :] = 0  # Zera a linha
                K_temp[:, index_Dy] = 0  # Zera a coluna
                K_temp[index_Dy, index_Dy] = 1  # Coloca 1 da diagonal

                F_temp[index_Dy] = 0

            if support.Rz:
                K_temp[index_Rz, :] = 0  # Zera a linha
                K_temp[:, index_Rz] = 0  # Zera a coluna
                K_temp[index_Rz, index_Rz] = 1  # Coloca 1 da diagonal

                F_temp[index_Rz] = 0

        # Resolve o sistema linear
        self.disp = np.linalg.solve(K_temp, F_temp)

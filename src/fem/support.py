from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node


@dataclass(frozen=True)
class Restriction:
    Dx: bool = False  # Restrição de deslocamento em x
    Dy: bool = False  # Restrição de deslocamento em y
    Rz: bool = False  # Restrição de rotação em z


class Support:
    _nodal: dict[Node, Restriction]  # Restrições aplicadas no nós

    def __init__(self) -> None:
        self._nodal = {}

    def add_nodal_support(self, node: Node, restriction: Restriction) -> None:
        """Adiciona um conjunto de restrição em um nó.

        Args:
            node (Node): O nó em que será aplicada a restrição.
            restriction (Restriction): O conjunto de restrição
        """
        self._nodal[node] = restriction

    def nodal(self) -> dict[Node, Restriction]:
        """Retor o conjunto de restrições nodais (condições de contorno)

        Returns:
            dict[Node, Restriction]: Conjunto de restrições nodais
                (condições de contorno)
        """
        return self._nodal

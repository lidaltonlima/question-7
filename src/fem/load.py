from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .element import Element
    from .node import Node


@dataclass(frozen=True)
class NodalLoad:
    """Representa uma carga pontual individual aplicada em um nó no sistema
    global.

    Attributes:
        Fx (float): Força na direção do eixo X.
        Fy (float): Força na direção do eixo Y.
        Mz (float): Momento fletor em torno do eixo Z.
    """

    Fx: float = 0.0
    Fy: float = 0.0
    Mz: float = 0.0


@dataclass(frozen=True)
class ConstantLoad:
    """Representa uma carga constante aplicada em uma barra no sistema local.

    Attributes:
        Fy (float): Força na direção do eixo Y.
    """

    Fy: float = 0.0


class LoadCase:
    name: str  # Nome do caso de carga
    _nodal: dict[Node, NodalLoad]  # Cargas nodais
    _distributed: dict[Element, ConstantLoad]  # Cargas constates de elemento

    def __init__(self, name: str) -> None:
        self.name = name
        self._nodal = {}
        self._distributed = {}

    def add_nodal_load(self, node: Node, load: NodalLoad) -> None:
        """Insere uma carga nodal

        Args:
            node (Node): Nó que possui a carga
            load (NodalLoad): Carga a ser inserida

        **OBS**:
            - Ao inserir uma carga nodal, se já existir uma carga, ela será
            substituída.
        """
        self._nodal[node] = load

    def add_constant_load(self, element: Element, load: ConstantLoad) -> None:
        """Insere uma carga constante em todo o elemento.

        Args:
            element (Element): Elemento
            load (ConstantLoad): Carga a ser inserida
        **OBS**:
            - Ao inserir uma carga nodal, se já existir uma carga, ela será
            substituída.
        """
        self._distributed[element] = load

    def nodal_loads(self) -> dict[Node, NodalLoad]:
        """Retorna o dicionário de cargas nodais.

        Returns:
            dict[Node, NodalLoad]: O dicionário de cargas nodais.
        """
        return self._nodal

    def element_loads(self) -> dict[Element, ConstantLoad]:
        """Retorna o dicionário de cargas constantes nos elementos

        Returns:
            dict[Element, ConstantLoad]: O dicionário de cargas constantes nos
            elementos

        **OBS**:
            - No momento só é possível inserir carga constante na direção y
            local
        """
        return self._distributed

    def __repr__(self) -> str:
        """Representação do objeto"""
        return f'{self.__class__.__name__}({self.name})'

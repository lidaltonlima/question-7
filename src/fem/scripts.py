from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from .element import Element
    from .load import LoadCase
    from .node import Node


def get_node_distance(node_i: Node, node_f: Node) -> float:
    """Calula a distância entre dois nós

    Args:
        node_i (Node): Nó inicial
        node_f (Node): Nó final

    Returns:
        float: A distância entre nós
    """
    dx = abs(node_f.x - node_i.x)  # Variação em "x"
    dy = abs(node_f.y - node_i.y)  # Variação em "y"

    return np.sqrt(dx**2 + dy**2, dtype=float)


def get_R(element: Element) -> NDArray:  # noqa: N802
    """Calcula a matriz de rotação do elemento

    Args:
        element (Element): Elemento para o qual a matriz será calculada

    Returns:
        NDArray: A matriz de rotação do elemento
    """
    dx = element.node_f.x - element.node_i.x  # Variação em "x"
    dy = element.node_f.y - element.node_i.y  # Variação em "y"
    L = element.length  # noqa: N806

    # Cossenos diretores
    cos0 = dx / L
    sin0 = dy / L

    R = np.zeros([6, 6])  # Inicia a matriz zerada  # noqa: N806

    # Calcula a parte do nó inicial
    R[0, 0] = cos0
    R[0, 1] = sin0
    R[1, 0] = -sin0
    R[1, 1] = cos0
    R[2, 2] = 1

    # Para o nó final o calculo é mesmo
    R[3:, 3:] = R[:3, :3]

    return R


def get_kl(element: Element) -> NDArray:
    """Calcula a matriz de rigidez do elemento no sistema local

    Args:
        element (Element): O elemento para o qual a matriz de calculada

    Returns:
        NDArray: A matriz de rigidez do elemento no sistema local
    """
    # Pega todas propriedades necessárias
    L = element.length  # noqa: N806
    A = element.section.A  # noqa: N806
    I = element.section.I  # noqa: E741, N806
    E = element.material.E  # noqa: N806

    # Incia com uma matriz nula
    kl = np.zeros([6, 6])

    # Calcula a Matriz
    # 1° Linha
    kl[0, 0] = (E * A) / L
    kl[0, 3] = -kl[0, 0]

    # 2° Linha
    kl[1, 1] = (12 * E * I) / L**3
    kl[1, 2] = (6 * E * I) / L**2
    kl[1, 4] = -kl[1, 1]
    kl[1, 5] = kl[1, 2]

    # 3° Linha
    kl[2, 1] = (6 * E * I) / L**2
    kl[2, 2] = (4 * E * I) / L
    kl[2, 4] = -kl[2, 1]
    kl[2, 5] = (2 * E * I) / L

    # 4° Linha
    kl[3, 0] = -(E * A) / L
    kl[3, 3] = -kl[3, 0]

    # 5° Linha
    kl[4, 1] = -(12 * E * I) / L**3
    kl[4, 2] = -(6 * E * I) / L**2
    kl[4, 4] = -kl[4, 1]
    kl[4, 5] = kl[4, 2]

    # 6° Linha
    kl[5, 1] = (6 * E * I) / L**2
    kl[5, 2] = (2 * E * I) / L
    kl[5, 4] = -kl[2, 1]
    kl[5, 5] = (4 * E * I) / L

    return kl


def get_K(nodes: list[Node], elements: list[Element]) -> NDArray:  # noqa: N802
    """Calcula a matriz de rigidez global

    Args:
        nodes (list[Node]): Todos os nós da estrutura
        elements (list[Element]): Todos os elementos da estrutura
    """
    order = len(nodes) * 3

    K = np.zeros([order, order])  # noqa: N806

    for element in elements:
        index_i = nodes.index(element.node_i)
        index_f = nodes.index(element.node_f)
        kg = element.kg

        add_kg(K, kg, index_i, index_f)

    return K


def add_kg(K: NDArray, kg: NDArray, index_i: int, index_f: int) -> None:  # noqa: N803
    """Adiciona a matriz de rigidez do elemento na matriz de rigidez global

    Args:
        K (NDArray): Matriz de rigidez globa
        kg (NDArray): Matriz de rigidez do elemento no sistema global
        index_i (int): Índice do nó inicial
        index_f (int): Índice do nó final
    """
    # A soma da contribuição é feita através de um fatiamento.
    # Assim não é necessário fazer um looping e perder desempenho.

    # Onde começa o índice daquele nó
    start_i = index_i * 3
    # Como tem 3 graus de liberdade basta somar 3 para pegar o índice final
    end_i = start_i + 3

    # O processo se repete para a segundo nó
    start_f = index_f * 3
    end_f = start_f + 3

    # Soma das contribuições
    K[start_i:end_i, start_i:end_i] += kg[:3, :3]  # k_ii
    K[start_i:end_i, start_f:end_f] += kg[:3, 3:]  # k_ij
    K[start_f:end_f, start_f:end_f] += kg[3:, 3:]  # k_jj
    K[start_f:end_f, start_i:end_i] += kg[3:, :3]  # k_ji


def get_F(  # noqa: N802
    nodes: list[Node], elements: list[Element], load_cases: list[LoadCase]
) -> NDArray:
    """Calcula o vetor de cargas nodais global.

    Args:
        nodes (list[Node]): Os nós da estrutura.
        elements (list[Element]): Os elementos da estrutura.
        load_cases (list[LoadCase]): Os casos de carga da estrutura.

    Returns:
        NDArray: O vetor de cargas nodais global.
    """
    F = np.zeros(len(nodes) * 3)  # noqa: N806

    for load_case in load_cases:
        # Adiciona as cargas nodais
        for node, load in load_case.nodal_loads().items():
            index_i = nodes.index(node) * 3
            index_f = index_i + 3
            F[index_i:index_f] += np.array([load.Fx, load.Fy, load.Mz])

        # Adiciona as cargas de elemento
        for element, load in load_case.element_loads().items():
            # Calcula as cargas nodais devido as cargas distribuídas no elemento  # noqa: E501
            element.distribute_to_nodal(load)

            # Pega as cargas nos nós do elemento a adiciona no vetor de cargas global  # noqa: E501
            # Nó inicial
            index_i = nodes.index(element.node_i) * 3
            index_f = index_i + 3
            F[index_i:index_f] += element.fg[:3]

            # Nó final
            index_i = nodes.index(element.node_f) * 3
            index_f = index_i + 3
            F[index_i:index_f] += element.fg[3:]

    return F

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np
from matplotlib.patches import Arc

if TYPE_CHECKING:
    from matplotlib.pyplot import Axes

    from .element import Element
    from .structure import Structure


def draw_efforts(
    ax: Axes,
    x: float,
    y: float,
    fx: float,
    fy: float,
    mz: float,
    color_fx: str = 'red',
    color_fy: str = 'green',
    color_mz: str = 'blue',
    head_width: float = 0.15,
    head_length: float = 0.15,
    zorder: int = 3,
) -> None:
    """Desenha as setas e valores dos esforços

    Args:
        ax (Axes): Eixo do matplotlib
        x (float): Posição x
        y (float): Posição y
        fx (float): Força em x
        fy (float): Força em y
        mz (float): Momento em z
        color_fx (str, optional): Cor da força em x. Defaults to 'red'.
        color_fy (str, optional): Cor da força em y. Defaults to 'green'.
        color_mz (str, optional): Cor do momento em z. Defaults to 'blue'.
        head_width (float, optional): Largura da seta. Defaults to 0.15.
        head_length (float, optional): Comprimento da seta. Defaults to 0.15.
        zorder (int, optional): Ondem de impressão. Defaults to 3.
    """
    # Seta
    size = 1

    if fx >= 0:
        ax.arrow(
            x - (size + head_length),
            y,
            size,
            0,
            head_width=head_width,
            head_length=head_length,
            fc=color_fx,
            ec=color_fx,
            width=0.02,
            zorder=zorder,
        )
    else:
        ax.arrow(
            x,
            y,
            -size,
            0,
            head_width=head_width,
            head_length=head_length,
            fc=color_fx,
            ec=color_fx,
            width=0.02,
            zorder=zorder,
        )

    if fy >= 0:
        ax.arrow(
            x,
            y - (size + head_length),
            0,
            size,
            head_width=head_width,
            head_length=head_length,
            fc=color_fy,
            ec=color_fy,
            width=0.02,
            zorder=zorder,
        )
    else:
        ax.arrow(
            x,
            y,
            0,
            -size,
            head_width=head_width,
            head_length=head_length,
            fc=color_fy,
            ec=color_fy,
            width=0.02,
            zorder=zorder,
        )

    if mz >= 0:
        ax.add_patch(
            Arc(
                (x, y),
                1,
                1,
                angle=-45,
                theta1=0,
                theta2=180,
                color=color_mz,
                linewidth=2,
            )
        )
        ax.arrow(
            x - 0.35,
            y + 0.35,
            -0.001,
            -0.001,
            head_width=head_width,
            head_length=head_length,
            fc=color_mz,
            ec=color_mz,
            width=0.02,
            zorder=zorder,
        )
    else:
        ax.add_patch(
            Arc(
                (x, y),
                1,
                1,
                angle=-45,
                theta1=0,
                theta2=180,
                color=color_mz,
                linewidth=2,
            )
        )
        ax.arrow(
            x + 0.35,
            y - 0.35,
            -0.001,
            -0.001,
            head_width=head_width,
            head_length=head_length,
            fc=color_mz,
            ec=color_mz,
            width=0.02,
            zorder=zorder,
        )

    # Texto para Fx
    ax.text(
        x - (size + head_length),
        y + 0.1,
        f'{fx:.2f} N',
        color=color_fx,
    )

    # Texto para Fy
    ax.text(
        x + 0.1,
        y - (size + head_length),
        f'{fy:.2f} N',
        color=color_fy,
    )

    # Texto para Mx
    ax.text(
        x + 0.4,
        y + 0.4,
        f'{mz:.2f} N*m',
        color=color_mz,
    )


def fb_diagram(
    ax: Axes,
    element: Element,
    diagram: Literal['Normal', 'Shear', 'Moment'],
    *,
    node_color: str = 'blue',
    element_color: str = 'orange',
) -> None:
    """Desenha os diagrams de esforços internos.

    Args:
        ax (Axes): Eixos do matplotlib
        element (Element): O elemento para desenha o esforços
        diagram (Literal[&#39;Normal&#39;, &#39;Shear&#39;, &#39;Moment&#39;]):
            O tipo de esforço
        node_color (str, optional): Cor dos nós na estrutura.
            Defaults to 'blue'.
        element_color (str, optional): Cor do elemento. Defaults to 'orange'.
    """
    stress = np.array(
        [
            -element.end_efforts[0],
            element.end_efforts[1],
            -element.end_efforts[2],
            element.end_efforts[3],
            -element.end_efforts[4],
            element.end_efforts[5],
        ]
    )
    # Configurações
    ax.set_xlabel('Comprimento (m)')

    # Nós
    ax.plot(
        [0, element.length],
        [0, 0],
        color=element_color,
        linewidth=3,
    )

    # Elementos
    ax.scatter(0, 0, color=node_color, zorder=2, s=100)
    ax.scatter(element.length, 0, color=node_color, zorder=2, s=100)

    # Diagramas
    text_color = 'black'
    if diagram == 'Normal':
        # Configurações
        ax.set_ylabel('Normal (N)')

        # Tensão Normal
        color = 'red'
        ax.plot([0, 0], [0, stress[0]], color=color)
        ax.plot(
            [element.length, element.length],
            [0, stress[3]],
            color=color,
        )
        ax.plot(
            [0, element.length],
            [stress[0], stress[3]],
            color=color,
        )

        # Textos
        ax.text(
            0,
            stress[0],
            f'{stress[0]:.2f}',
            color=text_color,
        )

        ax.text(
            element.length,
            stress[3],
            f'{stress[3]:.2f}',
            color=text_color,
            horizontalalignment='right',
        )

    if diagram == 'Shear':
        # Configurações
        ax.set_ylabel('Cortante (N)')

        # Tensão Cisalhante
        color = 'green'
        ax.plot([0, 0], [0, stress[1]], color=color)
        ax.plot(
            [element.length, element.length],
            [0, stress[4]],
            color=color,
        )
        ax.plot(
            [0, element.length],
            [stress[1], stress[4]],
            color=color,
        )

        # Textos
        ax.text(
            0,
            stress[1],
            f'{stress[1]:.2f}',
            color=text_color,
        )

        ax.text(
            element.length,
            stress[4],
            f'{stress[4]:.2f}',
            color=text_color,
            horizontalalignment='right',
        )

    if diagram == 'Moment':
        # Configurações
        ax.set_ylabel('Momento Fletor (N*m)')

        # Momento fletor
        color = 'tab:cyan'
        ax.plot([0, 0], [0, stress[2]], color=color)
        ax.plot(
            [element.length, element.length],
            [0, stress[5]],
            color=color,
        )
        ax.plot(
            [0, element.length],
            [stress[2], stress[5]],
            color=color,
        )

        # Textos
        ax.text(
            0,
            stress[2],
            f'{stress[2]:.2f}',
            color=text_color,
        )

        ax.text(
            element.length,
            stress[5],
            f'{stress[5]:.2f}',
            color=text_color,
            horizontalalignment='right',
        )


def fb_reactions(
    ax: Axes,
    element: Element,
    node_color: str = 'blue',
    element_color: str = 'orange',
) -> None:
    """Desenha o diagram de corpo livre

    Args:
        ax (Axes): Eixo do matplotlib
        element (Element): Elemento para ver o diagrama
        node_color (str, optional): Cor dos nós. Defaults to 'blue'.
        element_color (str, optional): Cor dos elementos. Defaults to 'orange'.
    """
    ax.set_aspect('equal')

    # Nós
    ax.plot(
        [0, element.length],
        [0, 0],
        color=element_color,
        linewidth=3,
    )

    # Elementos
    ax.scatter(0, 0, color=node_color, zorder=2, s=100)
    ax.scatter(element.length, 0, color=node_color, zorder=2, s=100)

    # Cargas no nó inicial
    draw_efforts(
        ax,
        0,
        0,
        fx=element.end_efforts[0],
        fy=element.end_efforts[1],
        mz=element.end_efforts[2],
    )

    # Cargas no nó inicial
    draw_efforts(
        ax,
        element.length,
        0,
        fx=element.end_efforts[3],
        fy=element.end_efforts[4],
        mz=element.end_efforts[5],
    )


def draw_structure(
    ax: Axes,
    structure: Structure,
    node_color: str = 'cyan',
    element_color: str = 'orange',
    text_color: str = 'black',
) -> None:
    for element in structure.elements:
        # Elementos
        ax.plot(
            [element.node_i.x, element.node_f.x],
            [element.node_i.y, element.node_f.y],
            color=element_color,
            linewidth=3,
            zorder=2,
        )

        x = (element.node_i.x + element.node_f.x) / 2
        y = (element.node_i.y + element.node_f.y) / 2
        ax.text(x, y, element.name, color=text_color, fontweight='bold')

    for node in structure.nodes:
        # Nós
        ax.scatter(
            node.x,
            node.y,
            color=node_color,
            zorder=3,
            s=100,
        )
        ax.text(node.x, node.y, node.name, color=text_color, fontweight='bold')

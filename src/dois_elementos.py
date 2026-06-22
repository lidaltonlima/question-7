from typing import Literal

import matplotlib.pyplot as plt
import numpy as np

import fem
import fem.view

np.set_printoptions(
    linewidth=110, formatter={'float_kind': lambda x: f'{x:.4e}'}
)


# =============================================================================
# Visualização
# =============================================================================
def view_plot(
    diagram: Literal[
        'Structure',
        'Reactions',
        'Normal',
        'Shear',
        'Moment',
    ],
) -> None:
    """Visualização da estrutura"""
    if diagram == 'Structure':
        fig, ax = plt.subplots(1, 1, layout='constrained')
        fig.canvas.manager.set_window_title('2 Elementos por Barra')
        fig.canvas.manager.window.state('zoomed')
        ax.grid()
        fem.view.draw_structure(ax, structure)
        plt.show()
    else:
        beam_a: plt.Axes
        beam_b: plt.Axes
        bar_a: plt.Axes
        bar_b: plt.Axes
        fig, ((beam_a, beam_b), (bar_a, bar_b)) = plt.subplots(
            2, 2, layout='constrained'
        )
        fig.canvas.manager.set_window_title('2 Elementos por Barra')
        fig.canvas.manager.window.state('zoomed')

        beam_a.set_title('Viga - Parte A')
        beam_b.set_title('Viga - Parte B')
        bar_a.set_title('Barra Inclinada - Parte A')
        bar_b.set_title('Barra Inclinada - Parte B')

        if diagram == 'Normal':
            fem.view.fb_diagram(beam_a, el1a, 'Normal')
            fem.view.fb_diagram(beam_b, el1b, 'Normal')
            fem.view.fb_diagram(bar_a, el2a, 'Normal')
            fem.view.fb_diagram(bar_b, el2b, 'Normal')

        elif diagram == 'Shear':
            fem.view.fb_diagram(beam_a, el1a, 'Shear')
            fem.view.fb_diagram(beam_b, el1b, 'Shear')
            fem.view.fb_diagram(bar_a, el2a, 'Shear')
            fem.view.fb_diagram(bar_b, el2b, 'Shear')

        elif diagram == 'Moment':
            beam_a.invert_yaxis()
            beam_b.invert_yaxis()
            bar_a.invert_yaxis()
            bar_b.invert_yaxis()
            fem.view.fb_diagram(beam_a, el1a, 'Moment')
            fem.view.fb_diagram(beam_b, el1b, 'Moment')
            fem.view.fb_diagram(bar_a, el2a, 'Moment')
            fem.view.fb_diagram(bar_b, el2b, 'Moment')

        elif diagram == 'Reactions':
            fem.view.fb_reactions(beam_a, el1a)
            fem.view.fb_reactions(beam_b, el1b)
            fem.view.fb_reactions(bar_a, el2a)
            fem.view.fb_reactions(bar_b, el2b)

        plt.show()


# =============================================================================
# Cálculo
# =============================================================================
# Estrutura (Classe que contém a todos objetos) *******************************
structure = fem.Structure()

# Materiais *******************************************************************
steel = fem.Material('steel', 205e9)  # Pa

# Seções **********************************************************************
# Viga
area = 1e4 * (1e-3) ** 2  # m**2
inertia = 5e8 * (1e-3) ** 4  # m**4
beam_sec = fem.Section('S1', area, inertia)

# Barra inclinada
area = 8e4 * (1e-3) ** 2  # m**2
inertia = 2.8e8 * (1e-3) ** 4  # m**4
bar_sec = fem.Section('S2', area, inertia)

# Nós *************************************************************************
# Cria os nós
n1 = fem.Node('N1', 0, 6)
ni1 = fem.Node('NI1', 5, 6)
n2 = fem.Node('N2', 10, 6)
ni2 = fem.Node('NI2', 12.5, 3)
n3 = fem.Node('N3', 15, 0)

# Adiciona na estrutura
structure.add_node(n1)
structure.add_node(ni1)
structure.add_node(n2)
structure.add_node(ni2)
structure.add_node(n3)

# Elementos *******************************************************************
# Cria o elementos finitos
el1a = fem.Element('B1A', n1, ni1, steel, beam_sec)
el1b = fem.Element('B1B', ni1, n2, steel, beam_sec)
el2a = fem.Element('B2A', n2, ni2, steel, bar_sec)
el2b = fem.Element('B2B', ni2, n3, steel, bar_sec)

# Adiciona na estrutura
structure.add_element(el1a)
structure.add_element(el1b)
structure.add_element(el2a)
structure.add_element(el2b)

# Cargas **********************************************************************
load_case = fem.LoadCase('LC1')
structure.add_load_case(load_case)

load_case.add_nodal_load(n2, fem.NodalLoad(Mz=100e3))
load_case.add_constant_load(el1a, fem.ConstantLoad(Fy=30e3))
load_case.add_constant_load(el1b, fem.ConstantLoad(Fy=30e3))

# Condições de contorno *******************************************************
support = fem.Support()
support.add_nodal_support(n1, fem.Restriction(Dx=True, Dy=True, Rz=True))
support.add_nodal_support(n3, fem.Restriction(Dx=True, Dy=True, Rz=True))
structure.add_support(support)

# =============================================================================
# Cálculo
# =============================================================================
structure.calculate()

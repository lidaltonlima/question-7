import matplotlib.pyplot as plt
import numpy as np

import fem
import fem.view

np.set_printoptions(
    linewidth=110, formatter={'float_kind': lambda x: f'{x:.4e}'}
)


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
n1a = fem.Node('N1A', 5, 6)
n2 = fem.Node('N2', 10, 6)
n2a = fem.Node('N2', 12.5, 3)
n3 = fem.Node('N3', 15, 0)

# Adiciona na estrutura
structure.add_node(n1)
structure.add_node(n2)
structure.add_node(n3)

# Elementos *******************************************************************
# Cria o elementos finitos
el1 = fem.Element('B1', n1, n2, steel, beam_sec)
el2 = fem.Element('B2', n2, n3, steel, bar_sec)

# Adiciona na estrutura
structure.add_element(el1)
structure.add_element(el2)

# Cargas **********************************************************************
load_case = fem.LoadCase('LC1')
structure.add_load_case(load_case)

load_case.add_nodal_load(n2, fem.NodalLoad(Mz=100e3))
load_case.add_constant_load(el1, fem.ConstantLoad(Fy=30e3))

# Condições de contorno *******************************************************
support = fem.Support()
support.add_nodal_support(n1, fem.Restriction(Dx=True, Dy=True, Rz=True))
support.add_nodal_support(n3, fem.Restriction(Dx=True, Dy=True, Rz=True))
structure.add_support(support)

# =============================================================================
# Cálculo
# =============================================================================
structure.calculate()

# =============================================================================
# Visualização
# =============================================================================
beam: plt.Axes
bar: plt.Axes
fig, (beam, bar) = plt.subplots(2, 1, layout='constrained')

beam.set_title('Viga')
bar.set_title('Barra Inclinada')
if False:
    fem.view.fb_diagram(beam, el1, 'Normal')
    fem.view.fb_diagram(bar, el2, 'Normal')

if False:
    fem.view.fb_diagram(beam, el1, 'Shear')
    fem.view.fb_diagram(bar, el2, 'Shear')

if False:
    fem.view.fb_diagram(beam, el1, 'Moment')
    fem.view.fb_diagram(bar, el2, 'Moment')

if False:
    fem.view.fb_reactions(beam, el1)
    fem.view.fb_reactions(bar, el2)

# plt.show()  # noqa: ERA001

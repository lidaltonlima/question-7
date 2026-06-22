import numpy as np

import fem

np.set_printoptions(precision=3)

# Materiais
steel = fem.Material(205e9)  # Pa

# Seções
# Viga
area = 10e4 * (10e-3) ** 2  # m**2
inertia = 5e8 * (10e-3) ** 4  # m**4
beam_sec = fem.Section(area, inertia)

# Barra inclinada
area = 8e4 * (10e-3) ** 2  # m**2
inertia = 2.8e8 * (10e-3) ** 4  # m**4
bar_sec = fem.Section(area, inertia)

# Nós
n1 = fem.Node(0, 6)
n2 = fem.Node(10, 6)
n3 = fem.Node(15, 0)

# Elementos
el1 = fem.Element(n1, n2, steel, beam_sec)
el2 = fem.Element(n2, n3, steel, bar_sec)

print(el2.R)

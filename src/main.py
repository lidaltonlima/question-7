import tkinter as tk

import matplotlib.pyplot as plt

import dois_elementos
import um_elemento

# Altera o tamanho global das fontes
plt.rcParams.update(
    {
        'font.size': 16,  # Tamanho base para textos
    }
)

# =============================================================================
# Inicialização da janela
# =============================================================================
root = tk.Tk()  # Cria a janela
root.title('QUESTÃO 7')  # Modifica o título

# Defina o tamanho da sua janela
width = 500
height = 250

# Obtenha a resolução do monitor
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calcule a posição central
pos_x = int(screen_width / 2 - width / 2)
pos_y = int(screen_height / 2 - height / 2)

# Defina a geometria com o tamanho e a posição (L x A + X + Y)
root.geometry(f'{width}x{height}+{pos_x}+{pos_y}')

# =============================================================================
# Botões para estrutura com malha de 1 elemento por barra
# =============================================================================
# Frame ***********************************************************************
frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, padx=10, pady=10)

# Título da coluna ************************************************************
tk.Label(frame1, text='1 Elemento', font='bold').pack(pady=5)

# Botões **********************************************************************
tk.Button(
    frame1,
    text='Estrutura',
    width=30,
    command=lambda: um_elemento.view_plot('Structure'),
).pack(pady=5)
tk.Button(
    frame1,
    text='Esforços',
    width=30,
    command=lambda: um_elemento.view_plot('Reactions'),
).pack(pady=5)
tk.Button(
    frame1,
    text='Diagrama N',
    width=30,
    command=lambda: um_elemento.view_plot('Normal'),
).pack(pady=5)
tk.Button(
    frame1,
    text='Diagrama V',
    width=30,
    command=lambda: um_elemento.view_plot('Shear'),
).pack(pady=5)
tk.Button(
    frame1,
    text='Diagrama M',
    width=30,
    command=lambda: um_elemento.view_plot('Moment'),
).pack(pady=5)

# =============================================================================
# Botões para estrutura com malha de 2 elemento por barra
# =============================================================================
# Frame ***********************************************************************
frame2 = tk.Frame(root)
frame2.pack(side=tk.RIGHT, padx=10, pady=10)

# Título da coluna ************************************************************
tk.Label(frame2, text='2 Elementos', font='bold').pack(pady=5)

# Botões **********************************************************************
tk.Button(
    frame2,
    text='Estrutura',
    width=30,
    command=lambda: dois_elementos.view_plot('Structure'),
).pack(pady=5)
tk.Button(
    frame2,
    text='Esforços',
    width=30,
    command=lambda: dois_elementos.view_plot('Reactions'),
).pack(pady=5)
tk.Button(
    frame2,
    text='Diagrama N',
    width=30,
    command=lambda: dois_elementos.view_plot('Normal'),
).pack(pady=5)
tk.Button(
    frame2,
    text='Diagrama V',
    width=30,
    command=lambda: dois_elementos.view_plot('Shear'),
).pack(pady=5)
tk.Button(
    frame2,
    text='Diagrama M',
    width=30,
    command=lambda: dois_elementos.view_plot('Moment'),
).pack(pady=5)


# =============================================================================
# Exibição
# =============================================================================
root.mainloop()

#@title **Código para comparación Cosmic Strings vs. Scars (2D)**
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm


# Configuración profesional
plt.style.use('seaborn-v0_8-poster')
plt.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12
})


# Parámetros físicos (ajustables)
BOX_SIZE = 10  # kpc
RESOLUTION = 200


# Generar coordenadas
x = np.linspace(-BOX_SIZE/2, BOX_SIZE/2, RESOLUTION)
y = np.linspace(-BOX_SIZE/2, BOX_SIZE/2, RESOLUTION)
X, Y = np.meshgrid(x, y)


# 1. Cosmic String (Singularidad 1D)
string_potential = np.zeros_like(X)
string_potential[(X > -0.1) & (X < 0.1)] = -1/np.sqrt(Y[(X > -0.1) & (X < 0.1)]**2 + 0.01)  # Suavizado ε=0.01


# 2. Scar (Curvatura de Weyl 4D)
scar_curvature = np.sin(2*np.pi*X/BOX_SIZE) * np.cos(2*np.pi*Y/BOX_SIZE) * np.exp(-(X**2 + Y**2)/(BOX_SIZE/2)**2)


# Crear figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=120)


# Panel izquierdo: Cosmic String
im1 = ax1.imshow(string_potential, 
                cmap='viridis', 
                norm=SymLogNorm(linthresh=0.1, vmin=-10, vmax=0),
                extent=[-BOX_SIZE/2, BOX_SIZE/2, -BOX_SIZE/2, BOX_SIZE/2])
ax1.set_title("Cosmic String\n(1D Singularity)", pad=20)
ax1.set_xlabel('x [kpc]')
ax1.set_ylabel('y [kpc]', labelpad=10)
cbar1 = fig.colorbar(im1, ax=ax1, shrink=0.8)
cbar1.set_label('Gravitational Potential\n(arb. units)', rotation=270, labelpad=20)


# Panel derecho: Scar
im2 = ax2.imshow(scar_curvature, 
                cmap='coolwarm', 
                vmin=-1, vmax=1,
                extent=[-BOX_SIZE/2, BOX_SIZE/2, -BOX_SIZE/2, BOX_SIZE/2])
ax2.set_title("Cosmic Scar\n(4D Weyl Curvature)", pad=20)
ax2.set_xlabel('x [kpc]')
ax2.set_ylabel('y [kpc]', labelpad=10)
cbar2 = fig.colorbar(im2, ax=ax2, shrink=0.8)
cbar2.set_label('Weyl Curvature\n(arb. units)', rotation=270, labelpad=20)


# Ajustes finales
plt.tight_layout(pad=3.0)


# Guardar para LaTeX (formato vectorial recomendado)
plt.savefig('scars_vs_strings.pdf', bbox_inches='tight', dpi=300)
plt.savefig('scars_vs_strings.png', bbox_inches='tight', dpi=300, transparent=True)


print("¡Figura guardada como 'scars_vs_strings.pdf' y 'scars_vs_strings.png'!")
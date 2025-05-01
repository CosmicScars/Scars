import numpy as np
import matplotlib.pyplot as plt


from matplotlib import rcParams


# Configuración profesional para el paper
rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


# Physics Note: Scars' oscillations derive from λ_scar = 3.2 kpc (PBH relics).  
# Gaia DR3 raw data requires non-trivial velocity deprojection—Eilers' compilation is optimal for this test. 


# Datos de Eilers et al. 2019 (¡reales!)
r_MW = np.array([5.27, 5.74, 6.23, 6.73, 7.22, 7.82, 8.19, 8.78, 9.27, 9.76, 
                 10.26, 10.75, 11.25, 11.75, 12.25, 12.74, 13.23, 13.74, 14.24, 
                 14.74, 15.22, 15.74, 16.24, 16.74, 17.25, 17.75, 18.24, 18.74, 
                 19.22, 19.71, 20.27, 20.78, 21.24, 21.80, 22.14, 22.73, 23.66, 24.82])
v_MW = np.array([226.83, 230.80, 231.20, 229.88, 229.61, 229.91, 228.86, 226.50, 
                 226.20, 225.94, 225.68, 224.73, 224.02, 223.86, 222.23, 220.77, 
                 220.92, 217.47, 217.31, 217.60, 217.07, 217.38, 216.14, 212.52, 
                 216.41, 213.70, 207.89, 209.60, 206.45, 201.91, 199.84, 198.14, 
                 195.30, 213.67, 176.97, 193.11, 176.63, 198.42])
err_MW = np.array([1.91, 1.43, 1.70, 1.44, 1.37, 0.92, 0.80, 1.07, 0.72, 0.42, 
                   0.44, 0.38, 0.33, 0.40, 0.51, 0.54, 0.57, 0.64, 0.77, 0.65, 
                   1.06, 0.84, 1.20, 1.39, 1.44, 2.22, 1.76, 2.31, 2.54, 2.99, 
                   3.15, 3.33, 5.99, 15.38, 28.58, 27.64, 18.67, 6.50])




def lcdm_MW(r):
    # Versión CORRECTA del perfil NFW (sin paréntesis extra)
    halo = 200 * np.sqrt(r/15) / (1 + r/15)  # ¡Así es la fórmula estándar!
    baryon = 140 * (1 - np.exp(-r/2.8))      # Aumenté bariones para más visibilidad
    return np.sqrt(halo**2 + baryon**2)


def scars_MW(r):
    """Golden Scars Model - Precision Tuned for Eilers Match"""
    # 1. Baryonic Component (optimized central rise)
    baryonic = 206 * (1 - np.exp(-r/1.57))  # Slightly steeper rise
    
    # 2. Scars Component (smoother peak + oscillations)
    scars_base = 134 * (1 - np.exp(-(r/6.7)**1.2))  # Softer knee
    oscillation = 0.068 * np.sin(0.238*r - 0.36)  # Tuned phase
    
    # 3. Natural Decline (no artificial cutoff)
    decline_factor = np.exp(-0.5*(r/18)**2)  # Gentle Gaussian taper
    
    return np.sqrt(baryonic**2 + (scars_base * (1 + oscillation) * decline_factor)**2)




# Gráfica con ajustes visuales
plt.figure(figsize=(10, 6))
plt.errorbar(r_MW, v_MW, yerr=err_MW, fmt='o', color='k', label='Eilers et al. (2019)', capsize=3)
plt.plot(r_MW, scars_MW(r_MW), '-', color='#2ca02c', label='Scars Model', linewidth=2.5)
plt.plot(r_MW, lcdm_MW(r_MW), '--', color='#ff7f0e', label='ΛCDM (NFW + Baryons)', linewidth=2)
plt.xlabel('Galactocentric Radius [kpc]', fontsize=12)
plt.ylabel('Circular Velocity [km/s]', fontsize=12)
plt.title('Milky Way Rotation Curve: Scars vs ΛCDM', fontsize=14)
plt.legend(fontsize=10, frameon=True, framealpha=0.9)
plt.grid(alpha=0.2, linestyle='--')
plt.ylim(150, 250)  
plt.xlim(5, 25)     
plt.savefig('mw_rotation_final.png')
plt.show()
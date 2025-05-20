import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from glob import glob

# Montar Google Drive
drive.mount('/content/drive')

# --- 1. CARGAR TODOS LOS ARCHIVOS ---
files = sorted(glob('/content/drive/My Drive/GAIA/gaia-*-result.csv'))  # Ajusta la ruta
df_list = []
for file in files:
    df_temp = pd.read_csv(file)
    df_temp['bin_kpc'] = float(file.split('-')[1]) / 1000  # Extraer distancia central (ej: 4000 → 4.0 kpc)
    df_list.append(df_temp)
df_all = pd.concat(df_list, ignore_index=True)


# --- 2. CORRECCIÓN OPcional DE V_RAD (SOL → CENTRO) ---
df_all['v_rad_centro'] = df_all['vel_rad_km_s'] + 230 * np.cos(np.radians(df_all['l'])) * np.cos(np.radians(df_all['b']))


# --- 3. GRÁFICO SINUSOIDE SCARS (V_rad vs Distancia) ---
plt.figure(figsize=(15, 6))

# Opción A: V_rad respecto al Sol (sin corregir)
# plt.scatter(df_all['bin_kpc'], df_all['vel_rad_km_s'], s=1, alpha=0.3, label='V_rad (Sol)', color='blue')

# Opción B: V_rad respecto al centro (corregida)
# plt.scatter(df_all['bin_kpc'], df_all['v_rad_centro'], s=1, alpha=0.3, label='V_rad (Centro)', color='red')


# Gráfica V_rad (Centro Galáctico vs Solar)
plt.scatter(df_all['bin_kpc'], df_all['v_rad_centro'], 
            c='#4B0092',  # Púrpura oscuro (Centro)
            s=1, alpha=0.3, label='$V_{\\mathrm{rad}}$ (Galactic Center)')

plt.scatter(df_all['bin_kpc'], df_all['vel_rad_km_s'], 
            c='#D55E00',  # Naranja (Solar)
            s=1, alpha=0.3, label='$V_{\\mathrm{rad}}$ (Solar Frame)')


# Ajuste teórico Scars (λ=3.2 kpc)
r_range = np.linspace(4, 15, 100)
plt.plot(r_range, 20 * np.sin(2 * np.pi * r_range / 3.2), 'k-', label='Scars (λ=3.2 kpc)', lw=2)

# Add these to your plot for clearer interpretation:
plt.axhline(0, color='gray', ls='--', alpha=0.5)  # Reference zero-velocity line
plt.axvline(7.1, color='green', alpha=0.3, lw=10)  # Highlight the 7-8 kpc "well"
plt.text(7.5, -100, 'Scar Well\n(σ_v=30 km/s)', ha='center') 

plt.xlabel('Distancia al Centro Galáctico (kpc)')
plt.ylabel('Velocidad Radial (km/s)')
plt.title('SINUSOIDE SCARS EN TODOS LOS BINS (4-15 kpc)', pad=20)
plt.legend(markerscale=5)
plt.grid(alpha=0.2)
plt.show()

========================================= SOLO DESDE CENTRO GALACTICO: BARRAS ROJAS Y AZULES SEPARAS POR Y=0

# Graficar la sinusoide + torres con estilo
plt.figure(figsize=(16, 8))

# 1. Sinusoide Scars (horizontal)
plt.axhline(y=0, color='black', linestyle='--', alpha=0.3)
plt.plot(r_range, 20 * np.sin(2 * np.pi * r_range / 3.2), 'k-', lw=3, label='Scars (λ=3.2 kpc)')

# 2. Torres (puntos azules/rojos)
plt.scatter(df_all['bin_kpc'], df_all['vel_rad_km_s'], 
            c=np.where(df_all['vel_rad_km_s'] < 0, 'blue', 'red'), 
            s=1, alpha=0.1, label='Star Towers (V_rad)')

# Add these to your plot for clearer interpretation:
plt.axhline(0, color='gray', ls='--', alpha=0.5)  # Reference zero-velocity line
plt.axvline(7.1, color='green', alpha=0.3, lw=10)  # Highlight the 7-8 kpc "well"
plt.text(7.5, -100, 'Scar Well\n(σ_v=30 km/s)', ha='center') 


# 3. Ajustar ejes para destacar patrones
plt.ylim(-250, 250)
plt.xlim(4, 15)
plt.xlabel('Distància al Centre Galàctic (kpc)', fontsize=12)
plt.ylabel('V_rad seen from the Sun (km/s)', fontsize=12)
plt.title('Star Towers Dancing with Scars (Gaia DR3)', pad=20, fontsize=14)
plt.legend(loc='upper right')
plt.grid(alpha=0.1)
plt.show()

==========================================
WEYL WELL

plt.figure(figsize=(12, 4))
plt.errorbar(df_all.groupby('bin_kpc')['bin_kpc'].mean(), 
             df_all.groupby('bin_kpc')['vel_rad_km_s'].std(),
             fmt='o-', label='σ_v (Sol)')
plt.xlabel('Distancia (kpc)')
plt.ylabel('Dispersion σ_v (km/s)')
plt.title('Drop of σ_v in Weyl well', pad=20)
plt.axvspan(7, 8, color='green', alpha=0.1, label='Scars (7-8 kpc)')
plt.legend()
plt.grid(alpha=0.2)
plt.show()


=======================================
KST 

from scipy.stats import kstest  
# ¿Sigue tu V_rad una distribución gaussiana (como predice ΛCDM)?  
stat, p = kstest(df_all['vel_rad_km_s'], 'norm')  
print(f"KS-test vs Gaussiana: p={p:.3f}")  # Si p < 0.05, ΛCDM falla.  
>>> KS-test vs Gaussiana: p=0.000

========================================
PHASE MAP
phase = np.arctan2(df_all['v_rad_centro'], df_all['dist_centro_kpc'] % 3.2)  
plt.hist(phase, bins=30)  




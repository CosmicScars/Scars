MILKY WAY - METALLICITY

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from google.colab import drive


# Montar Google Drive
drive.mount('/content/drive')


# Cargar datos  
df = pd.read_csv('/content/drive/My Drive/GAIAMETAL/consolidado_con_metalicidad.csv')  


# Configuración  
plt.figure(figsize=(12, 4))  
plt.hexbin(df['dist_centro_kpc'], df['feh'], gridsize=100, cmap='inferno', bins='log')  
plt.colorbar(label='Nº estrellas')  
plt.axvspan(7, 8, color='green', alpha=0.1, label='Scar')  
plt.xlabel('Distancia al centro (kpc)'); plt.ylabel('[Fe/H]')  
plt.ylim(-2, 0.5); plt.grid(alpha=0.2)
===========
# Agrupar por bin de 0.1 kpc y calcular percentiles de [Fe/H]
import numpy as np
bins = np.arange(4, 20.1, 0.1)  
df['dist_bin'] = pd.cut(df['dist_centro_kpc'], bins=bins)  
stats = df.groupby('dist_bin')['feh'].agg(['median', 'std', 'count'])  


# Plotear mediana ± desviación estándar  
plt.figure(figsize=(12, 4))  
plt.errorbar(bins[:-1], stats['median'], yerr=stats['std'], fmt='o', ms=3, alpha=0.5)  
plt.axvspan(7, 8, color='green', alpha=0.1)  
plt.xlabel('Distance (kpc)'); plt.ylabel('[Fe/H] median ± σ')

========================
# Comparar distribuciones de [Fe/H] dentro/fuera del Scar
plt.figure(figsize=(10, 5))
plt.hist(df[df['dist_centro_kpc'].between(7,8)]['feh'], bins=50, alpha=0.5,
         density=True, label='7-8 kpc (Scar)')
plt.hist(df[df['dist_centro_kpc'].between(4,6)]['feh'], bins=50, alpha=0.5,
         density=True, label='4-6 kpc')
plt.xlabel('[Fe/H]'); plt.ylabel('Normalized density')
plt.legend()
plt.title('The Scar selects metal-poor stars')

================================
plt.hist(df[df['dist_centro_kpc'].between(7,8)]['feh'], bins=50, density=True,  
         alpha=0.7, label='7-8 kpc (Scar)', color='#d62728')  # Rojo oscuro  
plt.hist(df[df['dist_centro_kpc'].between(6,7)]['feh'], bins=50, density=True,  
         alpha=0.5, label='6-7 kpc', color='#1f77b4')  # Azul  
plt.axvline(x=-0.25, ls=':', c='gray', label='Δ[Fe/H] = 0.25 dex')  # Línea de referencia  
plt.xlabel('[Fe/H]'); plt.ylabel('Normalized Density')  
plt.legend()  

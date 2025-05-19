import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from google.colab import drive
import glob
import re


# Configuración interactiva (¡EDITA ESTO!)
RANGO_KPC = (6.0, 6.9)  # returns the 4 graphs within this kpc range
VEL_MAX_KM_S = 40       # Límite para estrellas "frías"


# Montar Google Drive
drive.mount('/content/drive')


def cargar_datos(rango_kpc):
    # Convertir kpc a pc
    rango_pc = (int(rango_kpc[0]*1000), int(rango_kpc[1]*1000))
   
    # Cargar archivos del rango
    files = []
    for pc in range(rango_pc[0], rango_pc[1], 100):
        files += glob.glob(f'/content/drive/My Drive/GAIA/gaia-{pc}-{pc+99}-result.csv')
   
    # Manejar caso especial >15kpc
    if rango_kpc[1] > 15:
        files += glob.glob('/content/drive/My Drive/GAIA/gaia-14999-result.csv')
   
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        # Extraer distancia del nombre del archivo
        if '14999' in file:
            df['dist_centro_kpc'] = 15.5  # Centro >15kpc
        else:
            pc_min = int(re.search(r'gaia-(\d+)', file).group(1))
            df['dist_centro_kpc'] = (pc_min + 50) / 1000  # Centro del bin en kpc
        dfs.append(df)
   
    if not dfs:
        print(f"❌ No hay archivos en el rango {rango_kpc[0]}-{rango_kpc[1]} kpc")
        return None
   
    return pd.concat(dfs)


def analizar_tramo(rango_kpc):
    data = cargar_datos(rango_kpc)
    if data is None:
        return
   
    print(f"⭐ Analizando {len(data)} estrellas en {rango_kpc[0]}-{rango_kpc[1]} kpc")
   
    # --- 1. Gráfico 3D ---
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(data['l'], data['b'], data['dist_centro_kpc'],
                   c=data['vel_rad_km_s'], s=1, cmap='coolwarm', alpha=0.7,
                   vmin=-VEL_MAX_KM_S, vmax=VEL_MAX_KM_S)
    ax.set_xlabel('Longitud galáctica (l)')
    ax.set_ylabel('Latitud galáctica (b)')
    ax.set_zlabel('Distancia al centro (kpc)')
    plt.colorbar(sc, label='Velocidad radial (km/s)')
    plt.title(f'Mapa 3D: {rango_kpc[0]}-{rango_kpc[1]} kpc | Scars Candidate', pad=20)
    plt.show()


    # --- 2. Histograma de velocidades ---
    plt.figure(figsize=(10, 6))
    plt.hist(data['vel_rad_km_s'], bins=np.linspace(-150, 150, 100),
             density=True, alpha=0.7, color='blue')
    plt.axvline(x=0, color='red', linestyle='--', label='v = 0')
    plt.xlim(-150, 150)
    plt.xlabel('Velocidad radial (km/s)')
    plt.ylabel('Densidad de estrellas')
    plt.title(f'Distribución de velocidades ({rango_kpc[0]}-{rango_kpc[1]} kpc)')
    plt.legend()
    plt.grid(True)
    plt.show()


    # --- 3. Dispersión por bin ---
    if rango_kpc[1] <= 15:  # Solo para bins regulares
        sigma_per_bin = data.groupby('dist_centro_kpc')['vel_rad_km_s'].std()
        plt.figure(figsize=(10, 6))
        sigma_per_bin.plot(marker='o', linestyle='--', color='green')
        plt.axhline(y=30, color='red', linestyle=':', label='Límite disco')
        plt.axhline(y=60, color='black', linestyle=':', label='Límite halo')
        plt.xlabel('Distancia al centro (kpc)')
        plt.ylabel('Dispersión (km/s)')
        plt.title(f'Dispersión por bin ({rango_kpc[0]}-{rango_kpc[1]} kpc)')
        plt.legend()
        plt.grid(True)
        plt.show()


    # --- 4. Mapa 2D de estrellas "frías" ---
    low_sigma = data[data['vel_rad_km_s'].abs() < VEL_MAX_KM_S]
    plt.figure(figsize=(12, 8))
    plt.scatter(low_sigma['l'], low_sigma['b'], s=1, alpha=0.5, color='purple')
    plt.xlabel('Longitud galáctica (l)')
    plt.ylabel('Latitud galáctica (b)')
    plt.title(f'Estrellas con |V_rad| < {VEL_MAX_KM_S} km/s ({rango_kpc[0]}-{rango_kpc[1]} kpc)')
    plt.grid(True)
    plt.show()


# ¡EJECUTA EL ANÁLISIS EN EL RANGO QUE QUIERAS!
analizar_tramo(RANGO_KPC)



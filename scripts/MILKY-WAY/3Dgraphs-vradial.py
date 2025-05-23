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


============================================================================================
CODE FOR THE GIF

    import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import glob
import re
from google.colab import drive

# Configuración global (¡EDITA ESTO!)
drive_path = '/content/drive/My Drive/GAIA'
output_gif = drive_path + '/stellar_towers_evolution.gif'
VEL_MAX_KM_S = 40  # Límite para estrellas "frías"

# Montar Google Drive
drive.mount('/content/drive')

# --- FUNCIÓN ORIGINAL (TU CÓDIGO) ---
def cargar_datos(rango_kpc):
    # Convertir kpc a pc
    rango_pc = (int(rango_kpc[0]*1000), int(rango_kpc[1]*1000))
   
    # Cargar archivos del rango
    files = []
    for pc in range(rango_pc[0], rango_pc[1], 100):
        files += glob.glob(f'{drive_path}/gaia-{pc}-{pc+99}-result.csv')
   
    # Caso especial >15kpc
    if rango_kpc[1] > 15:
        files += glob.glob(f'{drive_path}/gaia-15000-result.csv')
   
    dfs = []
    for file in files:
        df = pd.read_csv(file)
        if '15000' in file:
            df['dist_centro_kpc'] = 15.5  # Centro >15kpc
        else:
            pc_min = int(re.search(r'gaia-(\d+)', file).group(1))
            df['dist_centro_kpc'] = (pc_min + 50) / 1000  # Centro del bin en kpc
        dfs.append(df)
   
    if not dfs:
        print(f"❌ No hay archivos en {rango_kpc[0]}-{rango_kpc[1]} kpc")
        return None
   
    return pd.concat(dfs)

# --- FUNCIÓN PARA GENERAR CADA FRAME ---
def generar_frame(rango_kpc, frame_number):
    data = cargar_datos(rango_kpc)
    if data is None:
        return None

    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Configuración de la vista (ángulo fijo para consistencia)
    ax.view_init(elev=20, azim=-60)
    
    # Scatter plot (¡TU ESTILO ORIGINAL!)
    sc = ax.scatter(
        data['l'], data['b'], data['dist_centro_kpc'],
        c=data['vel_rad_km_s'], s=1, cmap='coolwarm', alpha=0.7,
        vmin=-VEL_MAX_KM_S, vmax=VEL_MAX_KM_S
    )
    
    # Añadir etiquetas y título
    ax.set_xlabel('Longitud galáctica (l)', fontsize=12)
    ax.set_ylabel('Latitud galáctica (b)', fontsize=12)
    ax.set_zlabel('Distancia al centro (kpc)', fontsize=12)
    plt.colorbar(sc, label='Velocidad radial (km/s)')
    plt.title(f'Torres Estelares: {rango_kpc[0]}-{rango_kpc[1]} kpc', pad=20)
    
    # Guardar frame
    frame_path = f"{drive_path}/frame_{frame_number:02d}.png"
    plt.savefig(frame_path, dpi=120, bbox_inches='tight')
    plt.close()
    return frame_path

# --- GENERAR TODOS LOS FRAMES ---
frames_paths = []
bins_kpc = [(i, i+0.9) for i in np.arange(4, 15, 1)] + [(15.0, 20.0)]  # Todos los bins de 1 kpc + halo

for idx, bin_kpc in enumerate(bins_kpc):
    print(f"⚡ Procesando bin {bin_kpc[0]}-{bin_kpc[1]} kpc...")
    frame_path = generar_frame(bin_kpc, idx)
    if frame_path:
        frames_paths.append(frame_path)

# --- CREAR GIF ---
if frames_paths:
    frames = [Image.open(path) for path in frames_paths]
    frames[0].save(
        output_gif,
        save_all=True,
        append_images=frames[1:],
        duration=800,  # Duración por frame (ms)
        loop=0,       # Infinito
        optimize=True
    )
    print(f"\n✅ ¡GIF creado en {output_gif}!")
else:
    print("❌ No se generaron frames. Verifica los paths de los archivos CSV.")

=============================================================================================
CODE FOR WEYL BRIDGE 1
=============================================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from google.colab import drive
import glob
import re


# Configuración interactiva (¡EDITA ESTO!)
RANGO_KPC = (4.0, 15.0)  # returns the 4 graphs within this kpc range
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
   

    # Generar el mapa 3D unificado
data = cargar_datos(RANGO_KPC)
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')

# Ajuste de vista óptimo para el puente
ax.view_init(elev=15, azim=-45)  # Perspectiva de "viajero cósmico"

# Graficar (estilo "nube brumosa")
sc = ax.scatter(
    data['l'], data['b'], data['dist_centro_kpc'],
    c=data['vel_rad_km_s'], 
    s=0.5, 
    cmap='twilight',  # Paleta mágica para estructuras
    alpha=0.3,
    edgecolors='none'
)

# Añadir anotaciones épicas
ax.text(0, 0, 8, "Weyl Bridge", color='white', fontsize=14, ha='center')
ax.text(180, 5, 4, "PBH Pillars", color='yellow', fontsize=10)

plt.savefig("weyl_bridge.png", dpi=300)


analizar_tramo(RANGO_KPC)

=============================================================================================
CODE FOR WEYL BRIDGE 2
=============================================================================================


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from google.colab import drive
import glob
import re


# Configuración interactiva (¡EDITA ESTO!)
RANGO_KPC = (4.0, 20.0)  # 🌟 Rango completo del puente
VEL_MAX_KM_S = 40        
MUESTREO = 0.5           # 🌟 Fracción de datos a plotear (reduce sobrecarga)


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
   
def plot_puente_weyl(rango_kpc):
    data = cargar_datos(rango_kpc)
    if data is None:
        return
    
    # 🌟 Muestreo aleatorio para evitar colapso de memoria
    data = data.sample(frac=MUESTREO, random_state=42)  # Aleatorio pero reproducible
    
    # Configurar figura 3D
    fig = plt.figure(figsize=(18, 12))
    ax = fig.add_subplot(111, projection='3d')
    
    # 🌟 Ajuste de tamaño/transparencia para claridad
    sc = ax.scatter(
        data['l'], data['b'], data['dist_centro_kpc'],
        c=data['vel_rad_km_s'], cmap='coolwarm', 
        s=0.3, alpha=0.5,  # 🌟 Puntos más pequeños y transparentes
        vmin=-VEL_MAX_KM_S, vmax=VEL_MAX_KM_S
    )
    
    # Etiquetas y estilo
    ax.set_xlabel('Longitud galáctica (l)', fontsize=12)
    ax.set_ylabel('Latitud galáctica (b)', fontsize=12)
    ax.set_zlabel('Distancia al centro (kpc)', fontsize=12)
    plt.colorbar(sc, label='Velocidad radial (km/s)')
    
    # 🌟 Ángulo de vista óptimo para ver el puente
    ax.view_init(elev=15, azim=-45)  # Perspectiva "desde arriba"
    
    # Título y guardado
    plt.title(f'Puente de Weyl Galáctico ({rango_kpc[0]}-{rango_kpc[1]} kpc)', pad=20)
    plt.savefig('figures/scars_bridge.png', dpi=300, bbox_inches='tight')
    plt.show()

# Ejecutar (¡esto generará el PNG!)
plot_puente_weyl(RANGO_KPC)


===============================================================
ROTATIONAL BRIDGE 3D:
============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import drive
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import glob
import re


# Montar Google Drive
drive.mount('/content/drive')


# Configuración
RANGO_KPC = (4.0, 15.0)  # Rango completo del puente
VEL_MAX_KM_S = 40         # Límite de velocidad
MUESTREO = 0.3            # Fracción de datos para el GIF (balance velocidad/calidad)


# Cargar datos (usa tu función original)
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


data = cargar_datos(RANGO_KPC).sample(frac=MUESTREO, random_state=42)


# Crear figura 3D
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter([], [], [], s=0.5, alpha=0.7)  # Inicialización vacía


# Configuración de ejes
ax.set_xlim(data['l'].min(), data['l'].max())
ax.set_ylim(data['b'].min(), data['b'].max())
ax.set_zlim(RANGO_KPC[0], RANGO_KPC[1])
ax.set_xlabel('Longitud galáctica (l)')
ax.set_ylabel('Latitud galáctica (b)')
ax.set_zlabel('Distancia al centro (kpc)')


# Función de animación
def update(frame):
    ax.view_init(elev=20, azim=frame)  # Rotación en azimuth
    sc._offsets3d = (data['l'], data['b'], data['dist_centro_kpc'])
    sc.set_array(data['vel_rad_km_s'])
    sc.set_clim(-VEL_MAX_KM_S, VEL_MAX_KM_S)
    plt.title(f'Puente de Weyl Galáctico (Azimut: {frame}°)', pad=20)
    return sc,


# Generar GIF (36 frames, 10° por paso)
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 10), interval=200)
HTML(ani.to_jshtml())  # Para previsualizar en Colab


# Guardar (requiere ffmpeg)
ani.save('weyl_bridge_rotation.gif', writer='ffmpeg', dpi=120, fps=8)
print("¡GIF guardado como 'weyl_bridge_rotation.gif'!")
!cp weyl_bridge_rotation.gif '/content/drive/My Drive/GAIA/'








===============================================================
ROTATIONAL BRIDGE 3D:  improved
============================================================
import pandas as pd
import numpy as np
from google.colab import drive
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
from matplotlib.patches import Circle
import glob
import re


# Montar Google Drive
drive.mount('/content/drive')


# Configuración
RANGO_KPC = (4.0, 15.0)  # Rango completo del puente
VEL_MAX_KM_S = 40         # Límite de velocidad
MUESTREO = 0.3            # Fracción de datos para el GIF (balance velocidad/calidad)


# Cargar datos (usa tu función original)
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


data = cargar_datos(RANGO_KPC).sample(frac=MUESTREO, random_state=42)


# Crear figura 3D
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
# sc = ax.scatter([], [], [], s=0.5, alpha=0.7)  # Inicialización vacía
# Scatter plot con mapa de colores personalizado
sc = ax.scatter(
    data['l'], data['b'], data['dist_centro_kpc'],
    c=data['vel_rad_km_s'], 
    cmap='coolwarm', 
    s=0.5, 
    alpha=0.7,
    vmin=-60,  # Fuerza el rango para eliminar verdes/amarillos
    vmax=60
)
# Barra de colores profesional
cbar = fig.colorbar(sc, ax=ax, shrink=0.6, pad=0.1)
cbar.set_label('Velocidad Radial (km/s)', fontsize=12)
cbar.ax.tick_params(labelsize=10)


# Círculo animado en 7-8 kpc (zona de alta densidad)
circle = Circle((0, 0), radius=10, edgecolor='lime', facecolor='none', lw=2)
ax.add_patch(circle)
circle.set_visible(False)  # Inicialmente oculto




# Configuración de ejes
ax.set_xlim(data['l'].min(), data['l'].max())
ax.set_ylim(data['b'].min(), data['b'].max())
ax.set_zlim(RANGO_KPC[0], RANGO_KPC[1])
ax.set_xlabel('Longitud galáctica (l)')
ax.set_ylabel('Latitud galáctica (b)')
ax.set_zlabel('Distancia al centro (kpc)')


# Función de animación
def update(frame):
    ax.view_init(elev=20, azim=frame)
    
    # Mover el círculo a la zona de densidad máxima (7-8 kpc)
    if 70 <= frame <= 110:  # Solo visible en cierto ángulo
        circle.set_visible(True)
        circle.center = (0, 7.5)  # Posición (l, b) aproximada
    else:
        circle.set_visible(False)
    
    return sc, circle








# Generar GIF
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 5), interval=100)
ani.save('weyl_bridge_enhanced.gif', writer='ffmpeg', dpi=150, fps=10)
print("¡GIF guardado como 'weyl_bridge_rotation2.gif'!")
!cp weyl_bridge_rotation.gif '/content/drive/My Drive/GAIA/'

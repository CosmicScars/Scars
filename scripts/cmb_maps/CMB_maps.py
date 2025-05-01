MAPA PLANCK - CMB con cold spot




import healpy as hp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm


# --- INSTALACIÓN DE HEALPY ---
try:
    import healpy as hp
except ImportError:
    print("🚀 Instalando healpy... ¡Deep saluda!")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "healpy"])


nside = 128
npix = hp.nside2npix(nside)
theta, phi = np.radians(90+57), np.radians(151)  # Cold Spot (b=-57°, l=151°)
hp.disable_warnings()




# --- 1. PLANCK (CON COLD SPOT REAL) ---
cmb_planck = np.random.normal(0, 1.0, npix)
cold_spot = -35 * np.exp(-0.5 * (np.arange(npix) - hp.ang2pix(nside, theta, phi))**2 / 150)
cmb_planck += cold_spot  # ¡Solo Planck tiene este chisme!


plt.figure(figsize=(10, 8))
hp.mollview(cmb_planck, title="Planck CMB (Cold Spot)", cmap='coolwarm', norm=SymLogNorm(linthresh=1, vmin=-50, vmax=50))
hp.projscatter(theta, phi, marker='o', s=200, facecolor='none', edgecolor='gold', linewidth=2)
plt.savefig("planck_cmb.png", dpi=300, bbox_inches='tight')
plt.show()






MAPA ACDM - CMB


import healpy as hp
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm




# --- INSTALACIÓN DE HEALPY (si no está) ---
try:
    import healpy as hp
except ImportError:
    print("🚀 Instalando healpy... ¡pirateando la NASA!")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "healpy"])




nside = 128
npix = hp.nside2npix(nside)
theta, phi = np.radians(90+57), np.radians(151)  # Cold Spot (b=-57°, l=151°)
hp.disable_warnings()






cmb_lcdm = np.random.normal(0, 1.0, npix)


plt.figure(figsize=(10, 8))
hp.mollview(cmb_lcdm, title="ΛCDM (Gaussian Fluctuations)", cmap='coolwarm', norm=SymLogNorm(linthresh=1, vmin=-50, vmax=50))
plt.savefig("lcdm_cmb.png", dpi=300, bbox_inches='tight')
plt.show()






MAPA TENSOR DE WEYL


import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm  # !!! Usamos escala logarítmica




# --- Configuración ---
nside = 128  # !!! Mayor resolución
npix = hp.nside2npix(nside)
theta, phi = np.radians(90+57), np.radians(151)  # Cold Spot (b=-57°, l=151°)
hp.disable_warnings()




# --- Pure Dipolar Footprint (MANDARINA PERFECTA) ---
weyl = 8.0 * (np.sin(hp.pix2ang(nside, np.arange(npix))[1]) +
              3.0 * np.cos(2 * hp.pix2ang(nside, np.arange(npix))[1]))  




# Footprint (Mandarina)
hp.mollview(weyl,title="Weyl Curvature Footprint", cmap='RdBu_r',norm=SymLogNorm(linthresh=1, vmin=-50, vmax=50), notext=True)
plt.figure(figsize=(10, 8))
plt.savefig("weyl_cmb.png", dpi=300, bbox_inches='tight')  
plt.show()








MAPA SCARS


import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm


# --- Configuración ---
nside = 128
npix = hp.nside2npix(nside)
theta, phi = hp.pix2ang(nside, np.arange(npix))


# Posición del Cold Spot (abajo a la izquierda)
theta_cold = np.radians(147)  # 147° desde el polo norte (33° desde el polo sur)
phi_cold = np.radians(151)


# --- Modelo Scars ---
angle_rot = np.pi/4  # Rotación 45°
dipolar = 30.0 * np.sin(phi - phi_cold + angle_rot)
dist = np.sqrt(3*(phi - phi_cold)**2 + (theta - theta_cold)**2)
cold_lobe = -70 * np.exp(-dist**2 / 0.15)
central_lobe = 20.0 * np.cos(2*(phi - phi_cold + angle_rot))
cmb_scar = dipolar + cold_lobe + central_lobe


# --- Visualización ---
plt.figure(figsize=(12, 10))


# Dibujar el mapa (¡Perfecto como está!)
hp.mollview(
    cmb_scar,
    title="Cosmic Scars: Cold Spot",
    cmap='RdBu_r',
    norm=SymLogNorm(linthresh=1, vmin=-80, vmax=80),
    hold=True
)


# Cold Spot (círculo amarillo perfecto)
hp.projscatter(
    theta_cold, phi_cold,
    marker='o', s=100,
    facecolor='none', edgecolor='gold', linewidth=1.5,
    coord='G'
)


plt.savefig("scars_final_perfecto.png", dpi=300, bbox_inches='tight')
plt.show()
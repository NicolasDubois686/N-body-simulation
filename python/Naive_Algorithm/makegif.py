import numpy as np
import pygame
import os
import re

def capture_frame(ecran):
    """Renvoie l'image courante de la fenêtre Pygame (H, L, 3) en uint8"""
    arr = pygame.surfarray.array3d(ecran)  # (L, H, 3)
    return np.transpose(arr, (1, 0, 2))    # (H, L, 3)

def nom_fichier_gif(systeme, n_particules, prefixe="naif", dossier="assets", extra=None):
    """ex : <prefixe>_N15_dt0.05_eps0.5_a15_M10_seed42_001.gif"""
    params = [
        f"N{n_particules}",
        f"dt{systeme.dt:g}",
        f"eps{systeme.softening:g}",
        f"a{systeme.a:g}",
        f"M{systeme.M_tot:g}",
    ]
    if extra: 
        params += [f"{k}{v:g}" if isinstance(v, (int, float)) else f"{k}{v}"
                   for k, v in extra.items()]
        
    base = f"{prefixe}_" + "_".join(params)
    os.makedires(dossier, exist_ok=True)
    
    motif = re.compile(re.escape(base) + r"_(\d+)\.gif$")
    numeros = [int(m.group(1)) for f in os.listdir(dossier)
               if (m := motif.match(f))]
    suivant = max(numeros, default=0) + 1
    
    return os.path.join(dossier, f"{base}_{suivant:03d}.gif")
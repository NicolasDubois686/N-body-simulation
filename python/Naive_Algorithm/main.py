import numpy as np
from initialisation import *
from affichage_simulation import *
from moteur_physique import *
from integrateur_numerique import *
from diagnostics import *
from affichage_diagnostics import *
from makegif import *
import imageio.v2 as imageio
import time

       
#############################
# Définition des constantes #
#############################

LARGEUR = 1380
HAUTEUR = 720
DUREE   = 100
NB_PARTICLES = 10
SUB_STEPS = 10

############################
# Initialisation affichage #
############################

camera = Camera3D(
    screen_width  = LARGEUR,
    screen_height = HAUTEUR,
    focal_length  = 5000
)

ecran = init_fenetre_rendu(LARGEUR, HAUTEUR, titre="Simulation N-corps - Plummer 3D")
clock = pygame.time.Clock()

#############################
# Initialisation du système #
#############################

systeme = n_body_system(
    particules = np.array([]),
    dt         = 0.05,
    softening  = 0.5,
    G          = 5,
    M_tot      = 10,
    a          = 15
)

init_systeme_Plummer(systeme, NB_PARTICLES)

#######################################################
# Copie du systeme pour avoir les données temporelles #
#######################################################

systeme_copy = systeme.copy()

################################
# Initialisation diagnostiques #
################################

d0 = diagnostics(systeme)
traceur = TraceurTempsReel(d0)
frame = 0

#########################
# Initialisation du GIF #
#########################

frames = []
CAPTURE_EVERY = 2
n_affichage = 0

##############################
#   N-corps Algorithm Save   #
##############################

afficher_particules_3d(systeme, camera, ecran)

nb_pas = 0
simulation_active = True
t = 0
calculer_toutes_les_forces(systeme)
while (t < DUREE and simulation_active) :
    
    for _ in range(SUB_STEPS):
        t += systeme.dt/2
        leapfrog_demi_kick(systeme)
        leapfrog_drift(systeme)
        calculer_toutes_les_forces(systeme)
        leapfrog_demi_kick(systeme)
        t += systeme.dt/2
        nb_pas += 1
        
    nb_in_screen = afficher_particules_3d(systeme, camera, ecran)
    
    # GIF
    n_affichage += 1 
    if n_affichage % CAPTURE_EVERY == 0 :
        frames.append(np.ascontiguousarray(capture_frame(ecran)[::2, ::2]))
    
    # Diagnostics
    traceur.ajouter(t, diagnostics(systeme))
    frame += 1
    if frame % 5 == 0 :
        traceur.rafraichir()
        traceur.capturer_frame()
    
    clock.tick(60)
    if nb_in_screen <= 2 * NB_PARTICLES / 3 :
        simulation_active = False
    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            simulation_active = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q :
                simulation_active = False

#############
# Fermeture #
#############

traceur.fermer()

# Simulation
chemin_sim = nom_fichier_gif(systeme, NB_PARTICLES, prefixe="naif_simulation")
ask_for_save(frames, fps=30, chemin=chemin_sim, answer=True)

# Graphes 
chemin_diag = nom_fichier_gif(systeme, NB_PARTICLES, prefixe="naif_diagnostics")
ask_for_save(traceur.images, fps=10, chemin=chemin_diag, answer=True)

##################################
#   N-corps Algorithm Not Save   #
##################################

# Performances temporelles
t0 = time.perf_counter()
nb_pas_copy = 0
t = 0
calculer_toutes_les_forces(systeme_copy)
while (t < DUREE and simulation_active and nb_pas_copy < nb_pas) :
    
    for _ in range(SUB_STEPS):
        t += systeme_copy.dt/2
        leapfrog_demi_kick(systeme_copy)
        leapfrog_drift(systeme_copy)
        calculer_toutes_les_forces(systeme_copy)
        leapfrog_demi_kick(systeme_copy)
        t += systeme_copy.dt/2
        nb_pas_copy += 1
        
    if nb_in_screen <= 2 * NB_PARTICLES / 3 :
        simulation_active = False

duree = time.perf_counter() - t0

print()
print(f"{nb_pas} pas en {duree:.3f} s "
      f"({1e3 * duree / nb_pas:.3f} ms/pas)")
print()

pygame.display.quit()
pygame.quit()

########################
# Vérification égalité #
########################

def etat(s):
    P = s.particles
    return (np.array([p.position for p in P]),
            np.array([p.velocity for p in P]))

pos_a, vel_a = etat(systeme)
pos_b, vel_b = etat(systeme_copy)

assert np.array_equal(pos_a, pos_b), "positions différentes"
assert np.array_equal(vel_a, vel_b), "vitesses différentes"
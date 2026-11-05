import numpy as np

def leapfrog_demi_kick_une_particule(systeme, particule):
    # Pas de temps
    dt = systeme.dt
    # Calcul de l'accélération
    acceleration = particule.force / particule.mass
    # Demi-kick
    particule.velocity += 0.5 * dt * acceleration
    
def leapfrog_demi_kick(systeme):
    for particule in systeme.particles :
        leapfrog_demi_kick_une_particule(systeme, particule)
        
def leapfrog_drift_une_particule(systeme, particule):
    # Pas de temps
    dt = systeme.dt
    # Drift
    particule.position += dt * particule.velocity
    
def leapfrog_drift(systeme):
    for particule in systeme.particles :
        leapfrog_drift_une_particule(systeme, particule) 
import numpy as np
from moteur_physique import calculer_toutes_les_forces_sur_une_particule

def mettre_a_jour_position_et_vitesse(systeme):
    """Met à jour les positions et vitesses de chaque particule à partir de la force accumulée F, en utilisant l'algorithme Leapfrog

    Args:
        systeme (n_body_system): état courant du système
    """
    
    # Pas de temps
    dt = systeme.dt
    
    # Calcul de la position suivante d'une particule
    def position_suivante_un_objet(particule, dt):
        
        # Calcul de l'accélération initiale
        acceleration = particule.force / particule.mass
        # Demi-kick
        particule.velocity += 0.5 * dt * acceleration
        # Drift
        particule.position += dt * particule.velocity
        # Nouvelle accélération
        calculer_toutes_les_forces_sur_une_particule(systeme, particule)
        acceleration = particule.force / particule.mass
        # Demi-kick
        particule.velocity += 0.5 * dt * acceleration
        
        """
        # Calcul des positions suivantes
        acceleration = particule.force / particule.mass
        # Calcul des vitesses suivantes
        particule.velocity += acceleration * dt
        # Modification des données
        particule.position += particule.velocity * dt
        # Application à chaque particule
        """
        
    for particule in systeme.particles :
        position_suivante_un_objet(particule, dt)
        
    return
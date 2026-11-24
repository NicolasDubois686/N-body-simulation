import numpy as np

class Particle:
    def __init__(self, position, velocity, mass, id, radius):
        self.position = position # np.array
        self.velocity = velocity # np.array
        self.force    = np.zeros(3)
        self.mass     = mass 
        self.id       = id
        self.radius   = radius
        
    def copy(self):
        p = Particle(self.position.copy(), self.velocity.copy(),
                     self.mass, self.id, self.radius)
        p.force = self.force.copy()
        return p
        
class n_body_system:
    def __init__(self, particules, dt, softening, G, M_tot, a):
        self.particles = particules
        self.dt        = dt
        self.softening = softening
        self.G         = G           # Constante gravitationnelle
        self.M_tot     = M_tot
        self.a         = a           # Rayon d'echelle de Plummer
        
    def copy(self):
        return n_body_system(
            particules = np.array([p.copy() for p in self.particles]),
            dt = self.dt, softening = self.softening,
            G = self.G, M_tot = self.M_tot, a = self.a,
        )

def init_systeme_Plummer(systeme, nb_particules):
    """Alloue la mémoire nécessaire pour le tableau de particules avec la méthode de Plummer et définit les constantes physiques globales 

    Args:
        systeme (n_body_systeme): systeme étudié
        nb_particules (int): nombre de corps
        M_tot (float): Masse totale du système
        a (float): rayon d'echelle de Plummer
        G (float): constante gravitationnelle
        dt (float): pas de temps
        softening (float): parametre d'adoucissement gravitationnel
    """
    
    M_tot = systeme.M_tot
    G     = systeme.G
    a     = systeme.a
    
    liste_alea = [np.random.uniform(0.1,1) for i in range(nb_particules)]
    tot = sum(liste_alea)
    liste_masse = [M_tot * (liste_alea[i] / tot) for i in range(nb_particules)]
    
    for i in range(nb_particules):
        objet = Particle(
            position = np.zeros(3),
            velocity = np.zeros(3),
            mass     = liste_masse[i],
            id       = i,
            radius   = liste_masse[i]**(1/3)
        )
        # génération de la position (r, theta, phi)
        u1 = np.random.uniform(0, 0.9)
        r = a / np.sqrt(u1 ** (-2/3) - 1)
        
        # Orientation spatiale isotrope
        theta = np.arccos(2 * np.random.uniform(0, 1) - 1)
        phi = 2 * np.pi * np.random.uniform(0, 1)
        
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)
        
        # génération de la vitesse
        v = np.sqrt(2 * G * M_tot / np.sqrt(r**2 + a**2))
        
        # Méthode de rejet pour trouver le facteur q = v / v_e
        while True :
            q = np.random.uniform(0, 1)
            g = q**2 * (1 - q**2)**3.5
            test = np.random.uniform(0, 0.1)
            if test <= g:
                break
        
        norme_v = q * v
        
        # Orientation de la vitesse isotrope
        theta_v = np.arccos(2 * np.random.uniform(0, 1) - 1)
        phi_v = 2 * np.pi * np.random.uniform(0, 1)
        
        vx = norme_v * np.sin(theta_v) * np.cos(phi_v)
        vy = norme_v * np.sin(theta_v) * np.sin(phi_v)
        vz = norme_v * np.cos(theta_v)
        
        # Stockage dans la particule
        objet.position = np.array([x, y, z])
        objet.velocity = np.array([vx, vy, vz])
         
        # Ajout au systeme
        systeme.particles = np.append(systeme.particles, objet)
    
    # Centrage pour éviter une dérive grossière
    # Recentrage pour éviter la convergence
    centre_masse    = sum([liste_masse[i]*systeme.particles[i].position / M_tot for i in range(nb_particules)])
    vitesse_moyenne = sum([liste_masse[i]*systeme.particles[i].velocity / M_tot for i in range(nb_particules)])
    for i in range(nb_particules):
        systeme.particles[i].position -= centre_masse
        systeme.particles[i].velocity -= vitesse_moyenne
    return

def init_systeme_Kuzmin(nb_particules, dt, sftening):
    """Alloue la mémoire nécessaire pour le tableau de particules avec la méthode de Kuzmin et définit les constantes physiques globales

    Args:
        nb_particules (int): nombre de corps
        dt (float): pas de temps
        sftening (float): parametre d'adoucissement gravitationnel
    """
    return

def init_systeme_Navarro_Frenk_White(nb_particules, dt, sftening):
    """Alloue la mémoire nécessaire pour le tableau de particules avec la méthode de Navarro-Frenk-White et définit les constantes physiques globales

    Args:
        nb_particules (int): nombre de corps
        dt (float): pas de temps
        sftening (float): parametre d'adoucissement gravitationnel
    """
    return

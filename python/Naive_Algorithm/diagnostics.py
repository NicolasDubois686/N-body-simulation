import numpy as np

def diagnostics(systeme) :
    """Grandeurs conservées et état global du système"""
    P_ = systeme.particles                     
    pos = np.array([p.position for p in P_])   
    vel = np.array([p.velocity for p in P_])   
    m = np.array([p.mass for p in P_])         
    G, eps = systeme.G, systeme.softening      
    M = m.sum()                                
    
    # Energie
        # K + U doit être bornée et oscillante (Leapfrog est sympleptique)
        # K et U évoluent en opposition de phase
        # Energie cinétique
    K = 0.5 * np.sum(m*np.sum(vel**2, axis=1))
        # Energie potentielle (avec le même softening que la force)
    diff = pos[:, None, :] - pos[None, :, :]                    
    d = np.sqrt((diff**2).sum(-1) + eps**2)                   
    iu = np.tiu_indices(len(m), 1)                            
    U = -G * np.sum((m[:, None] * m[None, :])[iu] / d[iu])
    
    # Impulsion totale
        # Doit être constante à la précision machine
    P = (m[:, None] * vel).sum(0)
    
    # Moment cinétique
        # Doit être constant 
    L = (m[:, None] * np.cross(pos, vel)).sum(0)
    
    # Centre de masse
        # Doit être nul à la précision machine
    com = (m[:, None] * pos).sum(0) / M
    
    # Virial(~1 à l'équilibre)
        # Doit valoir ~1 à l'équilbre (moyenne temporelle, influence de eps, fluctuation pour beaucoup de particules)
    vir = 2 * K /abs(U)
    
    return {
        "K": K, "U": U, "E": K+U,
        "P": P, "L": L, "com": com,
        "virial": vir,
    }
    return
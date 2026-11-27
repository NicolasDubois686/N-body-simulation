
""" https://arborjs.org/docs/barnes-hut """
""" https://jheer.github.io/barnes-hut/ """

# Structure d'un objet
    # id
    # masse
    # coordonées
    # vitesse
    # résultante des forces

# Structure de l'arbre
    # Coordonnées du somment principal
    # Longueur des côtés
    # Masse de l'espace
    # Centre de gravité
    # Division suivante

# Construction de l'arbre
    # Si le noeud X est vide
        # Mettre l'objet dans ce noeud       
    # Si le noeud X est externe
        # Scinder le cube en 8 cubes égaux
        # Créer les 8 nouveaux noeuds
        # Ajouter les 2 objets dans le le bon noeud récursivement
  
# Calculer les masses et les centres de masse par un algorithme de parcours en 
    # Parcours en profondeur post ordre
    # Si feuille :
        # Centre de masse = position objet
        # Masse noeud = masse objet
        # Fin de l'appel de la fonction
    # Masse noeud = 0
    # Pour chaque fils du noeud :
        # appel récursif pour calculer le centre de masse et la masse du noeud fils
        # Masse noeud += masse objet
    # centre de masse = barycentre des centres de masse
     
# Calcul des forces opérant sur un objet
    # Si le noeud actuel est une feuille (et non celui dont on veut calculer la résultante)
        # Ajouter la force à la résultante
    # s : largeure du noeud analysé
    # d : distance entre l'objet et le centre de gravité du noeud
    # Sinon si s/d < theta
        # Considérer ce noeud interne comme une feuille et ajouter directement la force calculée à partir du centre de masse et de la masse
    # Sinon 
        # Relancer l'algorithme récursivement sur chacun des 8 noeud fils


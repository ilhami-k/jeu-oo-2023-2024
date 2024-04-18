### Classe `Personnage`
- Attributs : vie, armure, vitesse, position
- Méthodes : se déplacer(), attaquer(), subirDégâts()
- Relations :
  - Classe de base pour `Joueur` et `Ennemi`

### Classe `Joueur` (hérite de `Personnage`)
- Attributs : score, inventaire, niveau, compétences spéciales
- Méthodes : gagnerExpérience(), utiliserObjet(), améliorerCompétences()
- Relations :
  - Interagit avec `Arme`, `Obstacle`, `Niveau`, `InterfaceUtilisateur`
  - Utilise des objets de `Inventaire`

### Classe `Ennemi` (hérite de `Personnage`)
- Attributs : type, comportement, butin
- Méthodes : patrouiller(), poursuivreJoueur(), attaquer()
- Relations :
  - Peut laisser tomber des objets pour `Loot`

### Classe `Arme`
- Attributs : dégâts, portée, cadence de tir, munitions
- Méthodes : tirer(), recharger(), changerArme()
- Relations :
  - Utilisée par `Joueur`

### Classe `Obstacle`
- Attributs : position, taille, matériel
- Méthodes : bloquerPassage(), fournirCouverture()
- Relations :
  - Peut interagir avec `Personnage`

### Classe `InterfaceUtilisateur`
- Attributs : santé du joueur, munitions, menu
- Méthodes : mettreÀJourAffichage(), afficherMenu()
- Relations :
  - Affiche les informations de `Joueur`

### Classe `Équipement` (nouvelle classe)
- Attributs : nom, bonusStatistiques, niveauAmélioration
- Méthodes : améliorer(), équiper()
- Relations :
  - Peut être contenu dans `Inventaire`
  - Utilisé par `Joueur`

### Classe `PNJVendeur` (nouvelle classe)
- Attributs : inventaire, prix
- Méthodes : vendre(), acheter()
- Relations :
  - Interagit avec `Joueur` pour transactions

### Classe `PNJDonneurQuête` (nouvelle classe)
- Attributs : listeQuêtes
- Méthodes : donnerQuête(), récompenser()
- Relations :
  - Donne des quêtes à `Joueur`

### Classe `MissionPrincipale` (nouvelle classe)
- Attributs : histoire, objectifs, récompenses
- Méthodes : débuterMission(), accomplirObjectif()
- Relations :
  - Guide le `Joueur` à travers le jeu

### Classe `Loot` (nouvelle classe)
- Attributs : rareté, type, valeur
- Méthodes : ramasser(), utiliser()
- Relations :
  - Peut être obtenu par `Joueur` après combat

### Classe `Inventaire` (nouvelle classe)
- Attributs : listeObjets, capacité
- Méthodes : ajouterObjet(), retirerObjet(), utiliserObjet()
- Relations :
  - Gère les objets de `Joueur`

### Classe `Statistique` (nouvelle classe)
- Attributs : force, agilité, intelligence
- Méthodes : augmenterStat(), diminuerStat()
- Relations :
  - Détermine les capacités de `Personnage`

### Classe `Consommable` (nouvelle classe)
- Attributs : effet, durée
- Méthodes : consommer()
- Relations :
  - Peut être utilisé par `Joueur` pour des effets temporaires

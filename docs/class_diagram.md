# Diagramme de Classes - Jeu d'Échecs

## Vue d'ensemble
Le jeu d'échecs est composé de plusieurs classes organisées selon les principes de la programmation orientée objet.

## Classes Principales

### 1. Piece (Classe Abstraite)
**Attributs:**
- `couleur` : str (blanc/noir)
- `position` : tuple (ligne, colonne)
- `a_bouge` : bool (pour le roque et l'en passant)

**Méthodes:**
- `mouvements_possibles(plateau)` : List[tuple] - Retourne tous les mouvements possibles
- `peut_se_deplacer(position_cible, plateau)` : bool - Valide un déplacement
- `__str__()` : str - Représentation textuelle de la pièce

### 2. Classes de Pièces Spécifiques (Héritent de Piece)
- **Pion** : Déplacement avant, capture en diagonale, promotion, en passant
- **Tour** : Déplacement horizontal/vertical
- **Cavalier** : Déplacement en L
- **Fou** : Déplacement diagonal
- **Reine** : Déplacement horizontal/vertical/diagonal
- **Roi** : Déplacement d'une case dans toutes les directions, roque

### 3. Plateau
**Attributs:**
- `grille` : List[List[Piece | None]] - Grille 8x8
- `pieces_capturees` : List[Piece] - Liste des pièces capturées

**Méthodes:**
- `initialiser()` : void - Place les pièces en position initiale
- `obtenir_piece(position)` : Piece | None - Retourne la pièce à une position
- `deplacer_piece(depart, arrivee)` : bool - Déplace une pièce
- `est_case_vide(position)` : bool - Vérifie si une case est vide
- `est_position_valide(position)` : bool - Vérifie si une position est sur le plateau
- `afficher()` : void - Affiche le plateau dans le terminal

### 4. Joueur
**Attributs:**
- `nom` : str - Nom du joueur
- `couleur` : str - Couleur des pièces (blanc/noir)

**Méthodes:**
- `saisir_coup()` : tuple - Demande au joueur de saisir un coup

### 5. Jeu
**Attributs:**
- `plateau` : Plateau - Le plateau de jeu
- `joueur_blanc` : Joueur - Joueur avec les pièces blanches
- `joueur_noir` : Joueur - Joueur avec les pièces noires
- `joueur_actuel` : Joueur - Le joueur dont c'est le tour
- `historique` : List[tuple] - Historique des coups
- `position_en_passant` : tuple | None - Position pour la prise en passant

**Méthodes:**
- `demarrer()` : void - Lance la partie
- `jouer_tour()` : void - Gère un tour de jeu
- `est_echec(couleur)` : bool - Vérifie si le roi est en échec
- `est_echec_et_mat(couleur)` : bool - Vérifie si c'est échec et mat
- `est_pat(couleur)` : bool - Vérifie si c'est pat
- `obtenir_tous_mouvements_legaux(couleur)` : List[tuple] - Retourne tous les mouvements légaux
- `effectuer_coup(depart, arrivee)` : bool - Effectue un coup
- `annuler_coup()` : bool - Annule le dernier coup
- `changer_joueur()` : void - Passe au joueur suivant

## Relations entre les Classes

```
                    Piece (abstraite)
                        |
        +---------------+---------------+
        |               |               |
      Pion          Cavalier         Tour
        |               |               |
      Fou            Reine            Roi

    Plateau
      |
      +-- contient 0..32 Piece
      
    Joueur
      |
      +-- joue avec 1 couleur
      
    Jeu
      |
      +-- contient 1 Plateau
      +-- contient 2 Joueur
      +-- gère Piece à travers Plateau
```

## Flux de Jeu

1. Création du Jeu avec initialisation du Plateau et des Joueurs
2. Boucle de jeu:
   - Affichage du plateau
   - Joueur actuel saisit un coup
   - Validation du coup (légal, ne met pas le roi en échec)
   - Exécution du coup
   - Vérification d'échec, échec et mat, ou pat
   - Changement de joueur
3. Fin de partie avec affichage du résultat

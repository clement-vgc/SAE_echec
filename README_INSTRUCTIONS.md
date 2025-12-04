# Jeu d'Échecs en Python

Un jeu d'échecs complet développé en Python, jouable dans le terminal pour deux joueurs locaux.

## Caractéristiques

- ✅ **Programmation Orientée Objet (POO)** : Architecture basée sur des classes
- ✅ **Code commenté** : Documentation complète en français
- ✅ **Tests unitaires** : Tests complets pour toutes les fonctionnalités
- ✅ **Validation des coups** : Vérification automatique de la légalité des mouvements
- ✅ **Détection d'échec** : Alerte quand le roi est en danger
- ✅ **Détection d'échec et mat** : Fin de partie automatique
- ✅ **Détection de pat** : Match nul détecté automatiquement
- ✅ **Mouvements spéciaux** :
  - Roque (petit et grand)
  - Prise en passant
  - Promotion du pion
- ✅ **Interface terminal** : Affichage visuel avec symboles Unicode

## Structure du Projet

```
SAE_echec/
├── docs/
│   └── class_diagram.md         # Diagramme de classes détaillé
├── src/
│   ├── __init__.py
│   ├── piece.py                 # Classes des pièces d'échecs
│   ├── plateau.py               # Classe du plateau de jeu
│   ├── joueur.py                # Classe du joueur
│   └── jeu.py                   # Logique principale du jeu
├── tests/
│   ├── __init__.py
│   ├── test_piece.py            # Tests des pièces
│   ├── test_plateau.py          # Tests du plateau
│   └── test_jeu.py              # Tests du jeu
├── main.py                      # Point d'entrée du jeu
└── README_INSTRUCTIONS.md       # Ce fichier
```

## Installation et Lancement

### Prérequis

- Python 3.6 ou supérieur

### Lancer le jeu

```bash
# Depuis le répertoire racine du projet
python3 main.py
```

ou

```bash
python main.py
```

### Exécuter les tests

```bash
# Tous les tests
python3 -m unittest discover tests

# Tests spécifiques
python3 -m unittest tests.test_piece
python3 -m unittest tests.test_plateau
python3 -m unittest tests.test_jeu
```

## Comment Jouer

### Format des Coups

Les coups sont entrés au format **notation algébrique** : `position_départ position_arrivée`

Exemples :
- `e2 e4` : Déplace la pièce de e2 vers e4
- `g1 f3` : Déplace le cavalier de g1 vers f3

### Notation de l'Échiquier

```
   a b c d e f g h
  ┌─────────────────┐
8 │ ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ │ 8
7 │ ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ │ 7
6 │ · · · · · · · · │ 6
5 │ · · · · · · · · │ 5
4 │ · · · · · · · · │ 4
3 │ · · · · · · · · │ 3
2 │ ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ │ 2
1 │ ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ │ 1
  └─────────────────┘
   a b c d e f g h
```

- **Colonnes** : a, b, c, d, e, f, g, h (de gauche à droite)
- **Lignes** : 1, 2, 3, 4, 5, 6, 7, 8 (de bas en haut)

### Symboles des Pièces

| Pièce    | Blanc | Noir |
|----------|-------|------|
| Roi      | ♔     | ♚    |
| Reine    | ♕     | ♛    |
| Tour     | ♖     | ♜    |
| Fou      | ♗     | ♝    |
| Cavalier | ♘     | ♞    |
| Pion     | ♙     | ♟    |

### Commandes Spéciales

- `abandon` : Abandonner la partie
- `historique` : Afficher l'historique des coups

### Règles Spéciales Implémentées

1. **Roque** :
   - Petit roque : Déplacer le roi de 2 cases vers la droite (ex: `e1 g1`)
   - Grand roque : Déplacer le roi de 2 cases vers la gauche (ex: `e1 c1`)
   - Conditions : Le roi et la tour n'ont pas bougé, pas de pièces entre eux, le roi n'est pas en échec

2. **Prise en passant** :
   - Capture spéciale du pion après un mouvement de 2 cases d'un pion adverse

3. **Promotion du pion** :
   - Quand un pion atteint la dernière ligne, il est automatiquement promu
   - Le joueur choisit la pièce de promotion (Reine, Tour, Fou ou Cavalier)

## Architecture du Code

### Classes Principales

1. **Piece** (abstraite) : Classe de base pour toutes les pièces
   - `Pion`, `Tour`, `Cavalier`, `Fou`, `Reine`, `Roi` : Classes concrètes héritant de Piece

2. **Plateau** : Gère l'échiquier et les pièces
   - Grille 8x8
   - Méthodes de manipulation des pièces
   - Affichage du plateau

3. **Joueur** : Représente un joueur
   - Nom et couleur
   - Saisie des coups

4. **Jeu** : Orchestration de la partie
   - Gestion des tours
   - Validation des coups
   - Détection des conditions de fin (échec et mat, pat)
   - Historique des coups

### Diagramme de Classes

Consultez `docs/class_diagram.md` pour le diagramme de classes complet.

## Tests

Le projet inclut une suite de tests complète :

- **test_piece.py** : Tests pour chaque type de pièce
  - Mouvements possibles
  - Validations
  - Symboles

- **test_plateau.py** : Tests du plateau
  - Initialisation
  - Manipulation des pièces
  - Détection de positions

- **test_jeu.py** : Tests de la logique du jeu
  - Échec et échec et mat
  - Pat
  - Validation des coups
  - Historique

Tous les tests peuvent être exécutés avec :
```bash
python3 -m unittest discover tests -v
```

## Exemple de Partie

```
╔══════════════════════════════════════════════════╗
║        JEU D'ÉCHECS - VERSION TERMINALE          ║
╚══════════════════════════════════════════════════╝

Nom du joueur 1 (blancs) [Joueur 1]: Alice
Nom du joueur 2 (noirs) [Joueur 2]: Bob

Alice joue avec les blancs
Bob joue avec les noirs

Format des coups: 'e2 e4' (de e2 vers e4)
Tapez 'abandon' pour abandonner
Tapez 'historique' pour voir l'historique des coups

   a b c d e f g h
  ┌─────────────────┐
8 │ ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ │ 8
7 │ ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ │ 7
6 │ · · · · · · · · │ 6
5 │ · · · · · · · · │ 5
4 │ · · · · · · · · │ 4
3 │ · · · · · · · · │ 3
2 │ ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ │ 2
1 │ ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ │ 1
  └─────────────────┘
   a b c d e f g h

Alice (blanc), entrez votre coup (ex: e2 e4): e2 e4
```

## Développement

### Ajouter de Nouvelles Fonctionnalités

1. Créer une nouvelle branche
2. Implémenter la fonctionnalité
3. Ajouter des tests
4. Documenter le code
5. Exécuter tous les tests

### Conventions de Code

- **Langue** : Français pour les commentaires et les noms de variables
- **Style** : PEP 8
- **Documentation** : Docstrings pour toutes les classes et méthodes
- **Tests** : Tests unitaires pour toute nouvelle fonctionnalité

## Auteur

Développé dans le cadre du projet SAE (Situation d'Apprentissage et d'Évaluation).

## Licence

Ce projet est à usage éducatif.

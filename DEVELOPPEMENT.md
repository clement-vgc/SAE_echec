# Notes de Développement

## Commandes Importantes

### Tests
```bash
# Exécuter tous les tests
python3 -m unittest discover tests -v

# Exécuter un test spécifique
python3 -m unittest tests.test_piece
python3 -m unittest tests.test_plateau
python3 -m unittest tests.test_jeu
```

### Lancement du jeu
```bash
python3 main.py
```

## Architecture du Code

### Hiérarchie des Classes
- **Piece** (classe abstraite de base)
  - Méthode partagée: `_mouvements_ligne_droite()` utilisée par Tour, Fou, et Reine
  - Classes concrètes: Pion, Tour, Cavalier, Fou, Reine, Roi

### Conventions du Projet
- **Langue**: Tous les commentaires et docstrings en français
- **Format de code**: PEP 8
- **Tests**: Tests unitaires pour toute nouvelle fonctionnalité

## Points Techniques Importants

### Validation du Roque
Le roque nécessite que le roi soit à sa position initiale (colonne 4). Cette vérification évite les erreurs d'indexation hors limites.

Voir: `src/piece.py` lignes 288-291 et 305-308

### En Passant
La logique d'en passant est centralisée dans la méthode `_effectuer_en_passant_sur_plateau()` pour éviter la duplication de code.

Voir: `src/jeu.py` lignes 280-293

### Copie du Plateau
La méthode `copier()` du plateau crée une copie complète de toutes les pièces avec leur état (`a_bouge`, position, etc.). Important pour la simulation des coups.

Voir: `src/plateau.py` lignes 218-237

## Résultats des Tests

38 tests au total:
- 14 tests pour les pièces
- 13 tests pour le plateau
- 11 tests pour la logique du jeu

Tous les tests passent avec succès.

## Sécurité

Aucune vulnérabilité détectée par l'analyse CodeQL.

## Fonctionnalités Implémentées

### Mouvements des Pièces
- ✅ Pion (avance, capture diagonale, en passant, promotion)
- ✅ Tour (horizontal, vertical)
- ✅ Cavalier (en L, peut sauter)
- ✅ Fou (diagonal)
- ✅ Reine (horizontal, vertical, diagonal)
- ✅ Roi (une case dans toutes les directions, roque)

### Règles du Jeu
- ✅ Validation des coups légaux
- ✅ Détection d'échec
- ✅ Détection d'échec et mat
- ✅ Détection de pat
- ✅ Historique des coups
- ✅ Abandon

### Interface Utilisateur
- ✅ Affichage du plateau avec symboles Unicode
- ✅ Notation algébrique (e2 e4)
- ✅ Messages d'erreur clairs
- ✅ Commandes spéciales (historique, abandon)

## Améliorations Futures Possibles

1. **Règles supplémentaires**:
   - Nulle par répétition (3 fois la même position)
   - Nulle par les 50 coups
   - Temps de réflexion

2. **Interface**:
   - Mode graphique (pygame, tkinter)
   - Interface web
   - Sauvegarde/chargement de parties

3. **Intelligence artificielle**:
   - IA simple (minimax)
   - Évaluation de position
   - Niveaux de difficulté

4. **Multijoueur**:
   - Jeu en réseau
   - Mode tournoi

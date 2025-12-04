"""
Module contenant les classes de pièces d'échecs.
Chaque pièce hérite de la classe abstraite Piece.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class Piece(ABC):
    """
    Classe abstraite représentant une pièce d'échecs.
    
    Attributs:
        couleur (str): La couleur de la pièce ('blanc' ou 'noir')
        position (Tuple[int, int]): Position actuelle (ligne, colonne)
        a_bouge (bool): Indique si la pièce a déjà bougé (pour roque et en passant)
    """
    
    def __init__(self, couleur: str, position: Tuple[int, int]):
        """
        Initialise une pièce.
        
        Args:
            couleur: La couleur de la pièce ('blanc' ou 'noir')
            position: Position initiale (ligne, colonne)
        """
        self.couleur = couleur
        self.position = position
        self.a_bouge = False
    
    @abstractmethod
    def mouvements_possibles(self, plateau) -> List[Tuple[int, int]]:
        """
        Retourne tous les mouvements possibles pour cette pièce.
        
        Args:
            plateau: Le plateau de jeu
            
        Returns:
            Liste des positions possibles (ligne, colonne)
        """
        pass
    
    @abstractmethod
    def symbole(self) -> str:
        """
        Retourne le symbole de la pièce pour l'affichage.
        
        Returns:
            Symbole de la pièce
        """
        pass
    
    def peut_se_deplacer(self, position_cible: Tuple[int, int], plateau) -> bool:
        """
        Vérifie si la pièce peut se déplacer vers la position cible.
        
        Args:
            position_cible: Position de destination (ligne, colonne)
            plateau: Le plateau de jeu
            
        Returns:
            True si le déplacement est valide, False sinon
        """
        return position_cible in self.mouvements_possibles(plateau)
    
    def __str__(self) -> str:
        """Retourne la représentation textuelle de la pièce."""
        return self.symbole()


class Pion(Piece):
    """Classe représentant un pion."""
    
    def symbole(self) -> str:
        """Retourne le symbole du pion."""
        return '♙' if self.couleur == 'blanc' else '♟'
    
    def mouvements_possibles(self, plateau) -> List[Tuple[int, int]]:
        """
        Retourne les mouvements possibles pour le pion.
        
        Le pion se déplace d'une case vers l'avant (deux cases lors du premier mouvement),
        et capture en diagonale.
        """
        mouvements = []
        ligne, colonne = self.position
        direction = -1 if self.couleur == 'blanc' else 1
        
        # Mouvement d'une case vers l'avant
        nouvelle_ligne = ligne + direction
        if plateau.est_position_valide((nouvelle_ligne, colonne)):
            if plateau.est_case_vide((nouvelle_ligne, colonne)):
                mouvements.append((nouvelle_ligne, colonne))
                
                # Mouvement de deux cases si premier mouvement
                if not self.a_bouge:
                    nouvelle_ligne_2 = ligne + 2 * direction
                    if plateau.est_case_vide((nouvelle_ligne_2, colonne)):
                        mouvements.append((nouvelle_ligne_2, colonne))
        
        # Captures diagonales
        for dc in [-1, 1]:
            nouvelle_ligne = ligne + direction
            nouvelle_colonne = colonne + dc
            if plateau.est_position_valide((nouvelle_ligne, nouvelle_colonne)):
                piece_cible = plateau.obtenir_piece((nouvelle_ligne, nouvelle_colonne))
                if piece_cible and piece_cible.couleur != self.couleur:
                    mouvements.append((nouvelle_ligne, nouvelle_colonne))
                
                # En passant
                if hasattr(plateau, 'position_en_passant') and plateau.position_en_passant:
                    if (nouvelle_ligne, nouvelle_colonne) == plateau.position_en_passant:
                        mouvements.append((nouvelle_ligne, nouvelle_colonne))
        
        return mouvements


class Tour(Piece):
    """Classe représentant une tour."""
    
    def symbole(self) -> str:
        """Retourne le symbole de la tour."""
        return '♖' if self.couleur == 'blanc' else '♜'
    
    def mouvements_possibles(self, plateau) -> List[Tuple[int, int]]:
        """
        Retourne les mouvements possibles pour la tour.
        
        La tour se déplace horizontalement et verticalement.
        """
        return self._mouvements_ligne_droite(plateau, [(0, 1), (0, -1), (1, 0), (-1, 0)])
    
    def _mouvements_ligne_droite(self, plateau, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Calcule les mouvements en ligne droite dans les directions données.
        
        Args:
            plateau: Le plateau de jeu
            directions: Liste de directions (delta_ligne, delta_colonne)
            
        Returns:
            Liste des positions possibles
        """
        mouvements = []
        ligne, colonne = self.position
        
        for d_ligne, d_colonne in directions:
            nouvelle_ligne, nouvelle_colonne = ligne + d_ligne, colonne + d_colonne
            
            while plateau.est_position_valide((nouvelle_ligne, nouvelle_colonne)):
                piece_cible = plateau.obtenir_piece((nouvelle_ligne, nouvelle_colonne))
                
                if piece_cible is None:
                    mouvements.append((nouvelle_ligne, nouvelle_colonne))
                else:
                    if piece_cible.couleur != self.couleur:
                        mouvements.append((nouvelle_ligne, nouvelle_colonne))
                    break
                
                nouvelle_ligne += d_ligne
                nouvelle_colonne += d_colonne
        
        return mouvements


class Cavalier(Piece):
    """Classe représentant un cavalier."""
    
    def symbole(self) -> str:
        """Retourne le symbole du cavalier."""
        return '♘' if self.couleur == 'blanc' else '♞'
    
    def mouvements_possibles(self, plateau) -> List[Tuple[int, int]]:
        """
        Retourne les mouvements possibles pour le cavalier.
        
        Le cavalier se déplace en forme de L.
        """
        mouvements = []
        ligne, colonne = self.position
        
        # Tous les déplacements en L possibles
        deplacements = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for d_ligne, d_colonne in deplacements:
            nouvelle_ligne = ligne + d_ligne
            nouvelle_colonne = colonne + d_colonne
            
            if plateau.est_position_valide((nouvelle_ligne, nouvelle_colonne)):
                piece_cible = plateau.obtenir_piece((nouvelle_ligne, nouvelle_colonne))
                
                if piece_cible is None or piece_cible.couleur != self.couleur:
                    mouvements.append((nouvelle_ligne, nouvelle_colonne))
        
        return mouvements


class Fou(Piece):
    """Classe représentant un fou."""
    
    def symbole(self) -> str:
        """Retourne le symbole du fou."""
        return '♗' if self.couleur == 'blanc' else '♝'
    
    def mouvements_possibles(self, plateau) -> List[Tuple[int, int]]:
        """
        Retourne les mouvements possibles pour le fou.
        
        Le fou se déplace en diagonale.
        """
        return self._mouvements_ligne_droite(plateau, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
    
    def _mouvements_ligne_droite(self, plateau, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Calcule les mouvements en ligne droite dans les directions données."""
        mouvements = []
        ligne, colonne = self.position
        
        for d_ligne, d_colonne in directions:
            nouvelle_ligne, nouvelle_colonne = ligne + d_ligne, colonne + d_colonne
            
            while plateau.est_position_valide((nouvelle_ligne, nouvelle_colonne)):
                piece_cible = plateau.obtenir_piece((nouvelle_ligne, nouvelle_colonne))
                
                if piece_cible is None:
                    mouvements.append((nouvelle_ligne, nouvelle_colonne))
                else:
                    if piece_cible.couleur != self.couleur:
                        mouvements.append((nouvelle_ligne, nouvelle_colonne))
                    break
                
                nouvelle_ligne += d_ligne
                nouvelle_colonne += d_colonne
        
        return mouvements


class Reine(Piece):
    """Classe représentant une reine."""
    
    def symbole(self) -> str:
        """Retourne le symbole de la reine."""
        return '♕' if self.couleur == 'blanc' else '♛'
    
    def mouvements_possibles(self, plateau) -> List[Tuple[int, int]]:
        """
        Retourne les mouvements possibles pour la reine.
        
        La reine combine les mouvements de la tour et du fou.
        """
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),  # Horizontal et vertical
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        return self._mouvements_ligne_droite(plateau, directions)
    
    def _mouvements_ligne_droite(self, plateau, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Calcule les mouvements en ligne droite dans les directions données."""
        mouvements = []
        ligne, colonne = self.position
        
        for d_ligne, d_colonne in directions:
            nouvelle_ligne, nouvelle_colonne = ligne + d_ligne, colonne + d_colonne
            
            while plateau.est_position_valide((nouvelle_ligne, nouvelle_colonne)):
                piece_cible = plateau.obtenir_piece((nouvelle_ligne, nouvelle_colonne))
                
                if piece_cible is None:
                    mouvements.append((nouvelle_ligne, nouvelle_colonne))
                else:
                    if piece_cible.couleur != self.couleur:
                        mouvements.append((nouvelle_ligne, nouvelle_colonne))
                    break
                
                nouvelle_ligne += d_ligne
                nouvelle_colonne += d_colonne
        
        return mouvements


class Roi(Piece):
    """Classe représentant un roi."""
    
    def symbole(self) -> str:
        """Retourne le symbole du roi."""
        return '♔' if self.couleur == 'blanc' else '♚'
    
    def mouvements_possibles(self, plateau) -> List[Tuple[int, int]]:
        """
        Retourne les mouvements possibles pour le roi.
        
        Le roi se déplace d'une case dans toutes les directions.
        Inclut également le roque si les conditions sont remplies.
        """
        mouvements = []
        ligne, colonne = self.position
        
        # Mouvements normaux (une case dans toutes les directions)
        for d_ligne in [-1, 0, 1]:
            for d_colonne in [-1, 0, 1]:
                if d_ligne == 0 and d_colonne == 0:
                    continue
                
                nouvelle_ligne = ligne + d_ligne
                nouvelle_colonne = colonne + d_colonne
                
                if plateau.est_position_valide((nouvelle_ligne, nouvelle_colonne)):
                    piece_cible = plateau.obtenir_piece((nouvelle_ligne, nouvelle_colonne))
                    
                    if piece_cible is None or piece_cible.couleur != self.couleur:
                        mouvements.append((nouvelle_ligne, nouvelle_colonne))
        
        # Roque (ajouté dans la logique du jeu pour vérifier les conditions complètes)
        if not self.a_bouge:
            # Petit roque (côté roi)
            if self._peut_roquer_petit(plateau):
                mouvements.append((ligne, colonne + 2))
            
            # Grand roque (côté reine)
            if self._peut_roquer_grand(plateau):
                mouvements.append((ligne, colonne - 2))
        
        return mouvements
    
    def _peut_roquer_petit(self, plateau) -> bool:
        """Vérifie si le petit roque est possible."""
        ligne, colonne = self.position
        
        # Vérifier que les cases entre le roi et la tour sont vides
        for col in range(colonne + 1, colonne + 3):
            if not plateau.est_case_vide((ligne, col)):
                return False
        
        # Vérifier que la tour n'a pas bougé
        tour = plateau.obtenir_piece((ligne, 7))
        if tour is None or not isinstance(tour, Tour) or tour.a_bouge:
            return False
        
        return True
    
    def _peut_roquer_grand(self, plateau) -> bool:
        """Vérifie si le grand roque est possible."""
        ligne, colonne = self.position
        
        # Vérifier que les cases entre le roi et la tour sont vides
        for col in range(colonne - 3, colonne):
            if not plateau.est_case_vide((ligne, col)):
                return False
        
        # Vérifier que la tour n'a pas bougé
        tour = plateau.obtenir_piece((ligne, 0))
        if tour is None or not isinstance(tour, Tour) or tour.a_bouge:
            return False
        
        return True

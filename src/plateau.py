"""
Module contenant la classe Plateau pour gérer l'échiquier.
"""

from typing import List, Tuple, Optional
from src.piece import Piece, Pion, Tour, Cavalier, Fou, Reine, Roi


class Plateau:
    """
    Classe représentant le plateau d'échecs.
    
    Attributs:
        grille (List[List[Optional[Piece]]]): Grille 8x8 contenant les pièces
        pieces_capturees (List[Piece]): Liste des pièces capturées
        position_en_passant (Optional[Tuple[int, int]]): Position pour la prise en passant
    """
    
    def __init__(self):
        """Initialise un plateau vide."""
        self.grille: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.pieces_capturees: List[Piece] = []
        self.position_en_passant: Optional[Tuple[int, int]] = None
    
    def initialiser(self):
        """Place toutes les pièces dans leur position initiale."""
        # Pions
        for col in range(8):
            self.grille[1][col] = Pion('noir', (1, col))
            self.grille[6][col] = Pion('blanc', (6, col))
        
        # Tours
        self.grille[0][0] = Tour('noir', (0, 0))
        self.grille[0][7] = Tour('noir', (0, 7))
        self.grille[7][0] = Tour('blanc', (7, 0))
        self.grille[7][7] = Tour('blanc', (7, 7))
        
        # Cavaliers
        self.grille[0][1] = Cavalier('noir', (0, 1))
        self.grille[0][6] = Cavalier('noir', (0, 6))
        self.grille[7][1] = Cavalier('blanc', (7, 1))
        self.grille[7][6] = Cavalier('blanc', (7, 6))
        
        # Fous
        self.grille[0][2] = Fou('noir', (0, 2))
        self.grille[0][5] = Fou('noir', (0, 5))
        self.grille[7][2] = Fou('blanc', (7, 2))
        self.grille[7][5] = Fou('blanc', (7, 5))
        
        # Reines
        self.grille[0][3] = Reine('noir', (0, 3))
        self.grille[7][3] = Reine('blanc', (7, 3))
        
        # Rois
        self.grille[0][4] = Roi('noir', (0, 4))
        self.grille[7][4] = Roi('blanc', (7, 4))
    
    def obtenir_piece(self, position: Tuple[int, int]) -> Optional[Piece]:
        """
        Retourne la pièce à une position donnée.
        
        Args:
            position: Position (ligne, colonne)
            
        Returns:
            La pièce à cette position ou None si la case est vide
        """
        ligne, colonne = position
        if self.est_position_valide(position):
            return self.grille[ligne][colonne]
        return None
    
    def placer_piece(self, piece: Piece, position: Tuple[int, int]):
        """
        Place une pièce à une position donnée.
        
        Args:
            piece: La pièce à placer
            position: Position de destination (ligne, colonne)
        """
        ligne, colonne = position
        self.grille[ligne][colonne] = piece
        piece.position = position
    
    def retirer_piece(self, position: Tuple[int, int]) -> Optional[Piece]:
        """
        Retire une pièce d'une position.
        
        Args:
            position: Position (ligne, colonne)
            
        Returns:
            La pièce retirée ou None
        """
        ligne, colonne = position
        piece = self.grille[ligne][colonne]
        self.grille[ligne][colonne] = None
        return piece
    
    def deplacer_piece(self, depart: Tuple[int, int], arrivee: Tuple[int, int]) -> Optional[Piece]:
        """
        Déplace une pièce d'une position à une autre.
        
        Args:
            depart: Position de départ (ligne, colonne)
            arrivee: Position d'arrivée (ligne, colonne)
            
        Returns:
            La pièce capturée (si une) ou None
        """
        piece = self.retirer_piece(depart)
        if piece is None:
            return None
        
        # Capturer la pièce à la position d'arrivée si elle existe
        piece_capturee = self.retirer_piece(arrivee)
        if piece_capturee:
            self.pieces_capturees.append(piece_capturee)
        
        # Placer la pièce à la nouvelle position
        self.placer_piece(piece, arrivee)
        piece.a_bouge = True
        
        return piece_capturee
    
    def est_case_vide(self, position: Tuple[int, int]) -> bool:
        """
        Vérifie si une case est vide.
        
        Args:
            position: Position (ligne, colonne)
            
        Returns:
            True si la case est vide, False sinon
        """
        return self.obtenir_piece(position) is None
    
    def est_position_valide(self, position: Tuple[int, int]) -> bool:
        """
        Vérifie si une position est valide sur le plateau.
        
        Args:
            position: Position (ligne, colonne)
            
        Returns:
            True si la position est valide, False sinon
        """
        ligne, colonne = position
        return 0 <= ligne < 8 and 0 <= colonne < 8
    
    def trouver_roi(self, couleur: str) -> Optional[Tuple[int, int]]:
        """
        Trouve la position du roi d'une couleur donnée.
        
        Args:
            couleur: Couleur du roi à trouver ('blanc' ou 'noir')
            
        Returns:
            Position du roi (ligne, colonne) ou None si non trouvé
        """
        for ligne in range(8):
            for colonne in range(8):
                piece = self.grille[ligne][colonne]
                if piece and isinstance(piece, Roi) and piece.couleur == couleur:
                    return (ligne, colonne)
        return None
    
    def obtenir_toutes_pieces(self, couleur: str) -> List[Piece]:
        """
        Retourne toutes les pièces d'une couleur donnée.
        
        Args:
            couleur: Couleur des pièces ('blanc' ou 'noir')
            
        Returns:
            Liste des pièces de cette couleur
        """
        pieces = []
        for ligne in range(8):
            for colonne in range(8):
                piece = self.grille[ligne][colonne]
                if piece and piece.couleur == couleur:
                    pieces.append(piece)
        return pieces
    
    def afficher(self):
        """Affiche le plateau dans le terminal."""
        print("\n   a b c d e f g h")
        print("  ┌─────────────────┐")
        
        for ligne in range(8):
            print(f"{8 - ligne} │", end="")
            for colonne in range(8):
                piece = self.grille[ligne][colonne]
                if piece:
                    print(f" {piece.symbole()}", end="")
                else:
                    # Afficher un damier avec des cases claires et foncées
                    if (ligne + colonne) % 2 == 0:
                        print(" ·", end="")
                    else:
                        print("  ", end="")
            print(f" │ {8 - ligne}")
        
        print("  └─────────────────┘")
        print("   a b c d e f g h\n")
    
    def copier(self) -> 'Plateau':
        """
        Crée une copie du plateau.
        
        Returns:
            Une nouvelle instance de Plateau avec le même état
        """
        nouveau_plateau = Plateau()
        
        # Copier la grille
        for ligne in range(8):
            for colonne in range(8):
                piece = self.grille[ligne][colonne]
                if piece:
                    # Créer une nouvelle instance de la même classe
                    nouvelle_piece = type(piece)(piece.couleur, (ligne, colonne))
                    nouvelle_piece.a_bouge = piece.a_bouge
                    nouveau_plateau.grille[ligne][colonne] = nouvelle_piece
        
        nouveau_plateau.position_en_passant = self.position_en_passant
        
        return nouveau_plateau

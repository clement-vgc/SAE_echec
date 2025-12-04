"""
Module contenant la classe Joueur.
"""

from typing import Tuple


class Joueur:
    """
    Classe représentant un joueur d'échecs.
    
    Attributs:
        nom (str): Nom du joueur
        couleur (str): Couleur des pièces du joueur ('blanc' ou 'noir')
    """
    
    def __init__(self, nom: str, couleur: str):
        """
        Initialise un joueur.
        
        Args:
            nom: Nom du joueur
            couleur: Couleur des pièces ('blanc' ou 'noir')
        """
        self.nom = nom
        self.couleur = couleur
    
    def saisir_coup(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Demande au joueur de saisir un coup.
        
        Format attendu: 'e2 e4' (de e2 vers e4)
        Les colonnes sont représentées par des lettres (a-h) et les lignes par des chiffres (1-8)
        
        Returns:
            Tuple contenant la position de départ et la position d'arrivée
            
        Raises:
            ValueError: Si le format de la saisie est invalide
        """
        while True:
            try:
                entree = input(f"{self.nom} ({self.couleur}), entrez votre coup (ex: e2 e4): ").strip().lower()
                
                # Vérifier le format
                parties = entree.split()
                if len(parties) != 2:
                    print("Format invalide. Utilisez le format: e2 e4")
                    continue
                
                depart_str, arrivee_str = parties
                
                # Convertir la notation d'échecs en indices de tableau
                depart = self._notation_vers_position(depart_str)
                arrivee = self._notation_vers_position(arrivee_str)
                
                return depart, arrivee
                
            except ValueError as e:
                print(f"Erreur: {e}. Réessayez.")
    
    def _notation_vers_position(self, notation: str) -> Tuple[int, int]:
        """
        Convertit une notation d'échecs (ex: 'e2') en position de tableau.
        
        Args:
            notation: Notation d'échecs (ex: 'e2')
            
        Returns:
            Position (ligne, colonne) dans le tableau
            
        Raises:
            ValueError: Si la notation est invalide
        """
        if len(notation) != 2:
            raise ValueError(f"Notation invalide: {notation}")
        
        colonne_char = notation[0]
        ligne_char = notation[1]
        
        if colonne_char not in 'abcdefgh':
            raise ValueError(f"Colonne invalide: {colonne_char}")
        
        if ligne_char not in '12345678':
            raise ValueError(f"Ligne invalide: {ligne_char}")
        
        # Convertir colonne (a=0, b=1, ..., h=7)
        colonne = ord(colonne_char) - ord('a')
        
        # Convertir ligne (1=7, 2=6, ..., 8=0) - inversé car ligne 8 est en haut
        ligne = 8 - int(ligne_char)
        
        return (ligne, colonne)
    
    @staticmethod
    def position_vers_notation(position: Tuple[int, int]) -> str:
        """
        Convertit une position de tableau en notation d'échecs.
        
        Args:
            position: Position (ligne, colonne)
            
        Returns:
            Notation d'échecs (ex: 'e2')
        """
        ligne, colonne = position
        colonne_char = chr(ord('a') + colonne)
        ligne_char = str(8 - ligne)
        return colonne_char + ligne_char

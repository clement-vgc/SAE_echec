"""
Module contenant la classe Jeu qui gère la logique du jeu d'échecs.
"""

from typing import List, Tuple, Optional
from src.plateau import Plateau
from src.joueur import Joueur
from src.piece import Piece, Pion, Tour, Roi, Reine


class Jeu:
    """
    Classe principale gérant la logique du jeu d'échecs.
    
    Attributs:
        plateau (Plateau): Le plateau de jeu
        joueur_blanc (Joueur): Joueur avec les pièces blanches
        joueur_noir (Joueur): Joueur avec les pièces noires
        joueur_actuel (Joueur): Le joueur dont c'est le tour
        historique (List[Tuple]): Historique des coups joués
        partie_terminee (bool): Indique si la partie est terminée
    """
    
    def __init__(self, nom_joueur1: str = "Joueur 1", nom_joueur2: str = "Joueur 2"):
        """
        Initialise une nouvelle partie.
        
        Args:
            nom_joueur1: Nom du premier joueur (blancs)
            nom_joueur2: Nom du deuxième joueur (noirs)
        """
        self.plateau = Plateau()
        self.plateau.initialiser()
        
        self.joueur_blanc = Joueur(nom_joueur1, 'blanc')
        self.joueur_noir = Joueur(nom_joueur2, 'noir')
        self.joueur_actuel = self.joueur_blanc
        
        self.historique: List[Tuple] = []
        self.partie_terminee = False
    
    def demarrer(self):
        """Lance la partie et gère la boucle de jeu principale."""
        print("=" * 50)
        print("         BIENVENUE AU JEU D'ÉCHECS")
        print("=" * 50)
        print(f"\n{self.joueur_blanc.nom} joue avec les blancs")
        print(f"{self.joueur_noir.nom} joue avec les noirs\n")
        print("Format des coups: 'e2 e4' (de e2 vers e4)")
        print("Tapez 'abandon' pour abandonner")
        print("Tapez 'historique' pour voir l'historique des coups\n")
        
        while not self.partie_terminee:
            self.jouer_tour()
        
        print("\n" + "=" * 50)
        print("         FIN DE LA PARTIE")
        print("=" * 50)
    
    def jouer_tour(self):
        """Gère un tour de jeu complet."""
        # Afficher le plateau
        self.plateau.afficher()
        
        # Vérifier les conditions de fin de partie
        if self.est_echec_et_mat(self.joueur_actuel.couleur):
            adversaire = self.joueur_noir if self.joueur_actuel == self.joueur_blanc else self.joueur_blanc
            print(f"\n*** ÉCHEC ET MAT ! {adversaire.nom} gagne ! ***")
            self.partie_terminee = True
            return
        
        if self.est_pat(self.joueur_actuel.couleur):
            print("\n*** PAT ! Match nul ! ***")
            self.partie_terminee = True
            return
        
        # Vérifier si le joueur est en échec
        if self.est_echec(self.joueur_actuel.couleur):
            print(f"\n⚠️  ÉCHEC ! Le roi {self.joueur_actuel.couleur} est en danger !")
        
        # Demander au joueur de saisir son coup
        while True:
            try:
                entree = input(f"\n{self.joueur_actuel.nom} ({self.joueur_actuel.couleur}), entrez votre coup (ex: e2 e4): ").strip().lower()
                
                # Commandes spéciales
                if entree == 'abandon':
                    adversaire = self.joueur_noir if self.joueur_actuel == self.joueur_blanc else self.joueur_blanc
                    print(f"\n{self.joueur_actuel.nom} abandonne. {adversaire.nom} gagne !")
                    self.partie_terminee = True
                    return
                
                if entree == 'historique':
                    self.afficher_historique()
                    continue
                
                # Analyser le coup
                parties = entree.split()
                if len(parties) != 2:
                    print("Format invalide. Utilisez le format: e2 e4")
                    continue
                
                depart = self._notation_vers_position(parties[0])
                arrivee = self._notation_vers_position(parties[1])
                
                # Effectuer le coup
                if self.effectuer_coup(depart, arrivee):
                    break
                    
            except ValueError as e:
                print(f"Erreur: {e}")
        
        # Changer de joueur
        self.changer_joueur()
    
    def effectuer_coup(self, depart: Tuple[int, int], arrivee: Tuple[int, int]) -> bool:
        """
        Effectue un coup si celui-ci est valide.
        
        Args:
            depart: Position de départ (ligne, colonne)
            arrivee: Position d'arrivée (ligne, colonne)
            
        Returns:
            True si le coup a été effectué, False sinon
        """
        # Vérifier que la position de départ contient une pièce du joueur actuel
        piece = self.plateau.obtenir_piece(depart)
        
        if piece is None:
            print("❌ Il n'y a pas de pièce à cette position.")
            return False
        
        if piece.couleur != self.joueur_actuel.couleur:
            print("❌ Cette pièce n'est pas la vôtre.")
            return False
        
        # Vérifier que le mouvement est dans les mouvements possibles
        if arrivee not in piece.mouvements_possibles(self.plateau):
            print("❌ Ce mouvement n'est pas valide pour cette pièce.")
            return False
        
        # Simuler le mouvement pour vérifier qu'il ne met pas le roi en échec
        plateau_test = self.plateau.copier()
        piece_test = plateau_test.obtenir_piece(depart)
        
        # Gérer l'en passant
        piece_capturee_en_passant = None
        if isinstance(piece, Pion) and arrivee == self.plateau.position_en_passant:
            # En passant: capturer le pion adverse
            ligne_arrivee, colonne_arrivee = arrivee
            direction = 1 if piece.couleur == 'blanc' else -1
            position_pion_capture = (ligne_arrivee + direction, colonne_arrivee)
            piece_capturee_en_passant = plateau_test.retirer_piece(position_pion_capture)
        
        plateau_test.deplacer_piece(depart, arrivee)
        
        if self._est_roi_en_echec(plateau_test, self.joueur_actuel.couleur):
            print("❌ Ce coup mettrait votre roi en échec.")
            return False
        
        # Gérer le roque
        if isinstance(piece, Roi) and abs(arrivee[1] - depart[1]) == 2:
            # C'est un roque
            ligne = depart[0]
            
            # Vérifier que le roi ne traverse pas une case en échec
            if arrivee[1] > depart[1]:  # Petit roque
                # Vérifier les cases intermédiaires
                for col in range(depart[1], depart[1] + 3):
                    plateau_intermediaire = self.plateau.copier()
                    roi_test = plateau_intermediaire.obtenir_piece(depart)
                    plateau_intermediaire.retirer_piece(depart)
                    plateau_intermediaire.placer_piece(roi_test, (ligne, col))
                    
                    if self._est_roi_en_echec(plateau_intermediaire, self.joueur_actuel.couleur):
                        print("❌ Le roi ne peut pas roquer en traversant une case en échec.")
                        return False
                
                # Déplacer la tour
                tour_depart = (ligne, 7)
                tour_arrivee = (ligne, 5)
            else:  # Grand roque
                # Vérifier les cases intermédiaires
                for col in range(depart[1] - 2, depart[1] + 1):
                    plateau_intermediaire = self.plateau.copier()
                    roi_test = plateau_intermediaire.obtenir_piece(depart)
                    plateau_intermediaire.retirer_piece(depart)
                    plateau_intermediaire.placer_piece(roi_test, (ligne, col))
                    
                    if self._est_roi_en_echec(plateau_intermediaire, self.joueur_actuel.couleur):
                        print("❌ Le roi ne peut pas roquer en traversant une case en échec.")
                        return False
                
                # Déplacer la tour
                tour_depart = (ligne, 0)
                tour_arrivee = (ligne, 3)
            
            # Effectuer le roque
            self.plateau.deplacer_piece(depart, arrivee)
            self.plateau.deplacer_piece(tour_depart, tour_arrivee)
            
            print("✓ Roque effectué")
        else:
            # Mouvement normal
            # Gérer l'en passant
            if isinstance(piece, Pion) and arrivee == self.plateau.position_en_passant:
                ligne_arrivee, colonne_arrivee = arrivee
                direction = 1 if piece.couleur == 'blanc' else -1
                position_pion_capture = (ligne_arrivee + direction, colonne_arrivee)
                pion_capture = self.plateau.retirer_piece(position_pion_capture)
                if pion_capture:
                    self.plateau.pieces_capturees.append(pion_capture)
                print("✓ Prise en passant")
            
            piece_capturee = self.plateau.deplacer_piece(depart, arrivee)
            
            if piece_capturee:
                print(f"✓ {piece_capturee.symbole()} capturé")
        
        # Réinitialiser la position en passant
        self.plateau.position_en_passant = None
        
        # Gérer la position en passant pour le prochain coup
        if isinstance(piece, Pion) and abs(arrivee[0] - depart[0]) == 2:
            # Le pion a avancé de deux cases, l'en passant est possible au prochain tour
            direction = -1 if piece.couleur == 'blanc' else 1
            self.plateau.position_en_passant = (arrivee[0] + direction, arrivee[1])
        
        # Gérer la promotion du pion
        if isinstance(piece, Pion):
            ligne_arrivee = arrivee[0]
            if (piece.couleur == 'blanc' and ligne_arrivee == 0) or \
               (piece.couleur == 'noir' and ligne_arrivee == 7):
                self._promouvoir_pion(arrivee)
        
        # Ajouter le coup à l'historique
        self.historique.append((depart, arrivee, piece))
        
        return True
    
    def _promouvoir_pion(self, position: Tuple[int, int]):
        """
        Gère la promotion d'un pion.
        
        Args:
            position: Position du pion à promouvoir
        """
        piece = self.plateau.obtenir_piece(position)
        if not piece:
            return
        
        print("\n🎉 Promotion du pion !")
        print("Choisissez la pièce de promotion:")
        print("1. Reine (Q)")
        print("2. Tour (R)")
        print("3. Fou (B)")
        print("4. Cavalier (N)")
        
        choix_valides = {'1': Reine, 'q': Reine, 'reine': Reine,
                         '2': Tour, 'r': Tour, 'tour': Tour,
                         '3': Fou, 'b': Fou, 'fou': Fou,
                         '4': Cavalier, 'n': Cavalier, 'cavalier': Cavalier}
        
        while True:
            choix = input("Votre choix: ").strip().lower()
            if choix in choix_valides:
                nouvelle_piece_classe = choix_valides[choix]
                break
            print("Choix invalide. Réessayez.")
        
        # Remplacer le pion par la nouvelle pièce
        from src.piece import Fou, Cavalier
        nouvelle_piece = nouvelle_piece_classe(piece.couleur, position)
        nouvelle_piece.a_bouge = True
        self.plateau.placer_piece(nouvelle_piece, position)
        
        print(f"✓ Pion promu en {nouvelle_piece.symbole()}")
    
    def est_echec(self, couleur: str) -> bool:
        """
        Vérifie si le roi d'une couleur est en échec.
        
        Args:
            couleur: Couleur du roi à vérifier
            
        Returns:
            True si le roi est en échec, False sinon
        """
        return self._est_roi_en_echec(self.plateau, couleur)
    
    def _est_roi_en_echec(self, plateau: Plateau, couleur: str) -> bool:
        """
        Vérifie si le roi est en échec sur un plateau donné.
        
        Args:
            plateau: Le plateau à vérifier
            couleur: Couleur du roi
            
        Returns:
            True si le roi est en échec, False sinon
        """
        position_roi = plateau.trouver_roi(couleur)
        if not position_roi:
            return False
        
        # Vérifier si une pièce adverse peut attaquer le roi
        couleur_adverse = 'noir' if couleur == 'blanc' else 'blanc'
        pieces_adverses = plateau.obtenir_toutes_pieces(couleur_adverse)
        
        for piece in pieces_adverses:
            if position_roi in piece.mouvements_possibles(plateau):
                return True
        
        return False
    
    def est_echec_et_mat(self, couleur: str) -> bool:
        """
        Vérifie si c'est échec et mat pour une couleur.
        
        Args:
            couleur: Couleur du joueur à vérifier
            
        Returns:
            True si c'est échec et mat, False sinon
        """
        # Doit être en échec
        if not self.est_echec(couleur):
            return False
        
        # Aucun mouvement légal possible
        return len(self.obtenir_tous_mouvements_legaux(couleur)) == 0
    
    def est_pat(self, couleur: str) -> bool:
        """
        Vérifie si c'est pat (stalemate) pour une couleur.
        
        Args:
            couleur: Couleur du joueur à vérifier
            
        Returns:
            True si c'est pat, False sinon
        """
        # Ne doit pas être en échec
        if self.est_echec(couleur):
            return False
        
        # Aucun mouvement légal possible
        return len(self.obtenir_tous_mouvements_legaux(couleur)) == 0
    
    def obtenir_tous_mouvements_legaux(self, couleur: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Retourne tous les mouvements légaux pour une couleur.
        
        Args:
            couleur: Couleur du joueur
            
        Returns:
            Liste de tuples (position_depart, position_arrivee)
        """
        mouvements_legaux = []
        pieces = self.plateau.obtenir_toutes_pieces(couleur)
        
        for piece in pieces:
            mouvements_possibles = piece.mouvements_possibles(self.plateau)
            
            for arrivee in mouvements_possibles:
                # Simuler le mouvement
                plateau_test = self.plateau.copier()
                plateau_test.deplacer_piece(piece.position, arrivee)
                
                # Vérifier si le roi serait en échec
                if not self._est_roi_en_echec(plateau_test, couleur):
                    mouvements_legaux.append((piece.position, arrivee))
        
        return mouvements_legaux
    
    def changer_joueur(self):
        """Passe au joueur suivant."""
        self.joueur_actuel = self.joueur_noir if self.joueur_actuel == self.joueur_blanc else self.joueur_blanc
    
    def afficher_historique(self):
        """Affiche l'historique des coups."""
        if not self.historique:
            print("Aucun coup joué pour l'instant.")
            return
        
        print("\n--- Historique des coups ---")
        for i, (depart, arrivee, piece) in enumerate(self.historique, 1):
            depart_notation = Joueur.position_vers_notation(depart)
            arrivee_notation = Joueur.position_vers_notation(arrivee)
            print(f"{i}. {piece.symbole()} {depart_notation} → {arrivee_notation}")
        print("---------------------------\n")
    
    def _notation_vers_position(self, notation: str) -> Tuple[int, int]:
        """
        Convertit une notation d'échecs en position.
        
        Args:
            notation: Notation d'échecs (ex: 'e2')
            
        Returns:
            Position (ligne, colonne)
        """
        if len(notation) != 2:
            raise ValueError(f"Notation invalide: {notation}")
        
        colonne_char = notation[0]
        ligne_char = notation[1]
        
        if colonne_char not in 'abcdefgh':
            raise ValueError(f"Colonne invalide: {colonne_char}")
        
        if ligne_char not in '12345678':
            raise ValueError(f"Ligne invalide: {ligne_char}")
        
        colonne = ord(colonne_char) - ord('a')
        ligne = 8 - int(ligne_char)
        
        return (ligne, colonne)

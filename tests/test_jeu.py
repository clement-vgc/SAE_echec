"""
Tests unitaires pour la classe Jeu.
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.jeu import Jeu
from src.piece import Pion, Tour, Roi, Reine


class TestJeu(unittest.TestCase):
    """Tests pour la classe Jeu."""
    
    def setUp(self):
        """Initialise un jeu avant chaque test."""
        self.jeu = Jeu("TestJoueur1", "TestJoueur2")
    
    def test_initialisation(self):
        """Test l'initialisation du jeu."""
        self.assertIsNotNone(self.jeu.plateau)
        self.assertIsNotNone(self.jeu.joueur_blanc)
        self.assertIsNotNone(self.jeu.joueur_noir)
        self.assertEqual(self.jeu.joueur_actuel, self.jeu.joueur_blanc)
        self.assertFalse(self.jeu.partie_terminee)
    
    def test_est_echec_position_initiale(self):
        """Test qu'il n'y a pas d'échec en position initiale."""
        self.assertFalse(self.jeu.est_echec('blanc'))
        self.assertFalse(self.jeu.est_echec('noir'))
    
    def test_est_echec_simple(self):
        """Test la détection d'un échec simple."""
        # Créer un plateau avec un roi blanc en échec
        self.jeu.plateau.grille = [[None for _ in range(8)] for _ in range(8)]
        
        roi_blanc = Roi('blanc', (7, 4))
        tour_noire = Tour('noir', (0, 4))
        
        self.jeu.plateau.placer_piece(roi_blanc, (7, 4))
        self.jeu.plateau.placer_piece(tour_noire, (0, 4))
        
        self.assertTrue(self.jeu.est_echec('blanc'))
        self.assertFalse(self.jeu.est_echec('noir'))
    
    def test_est_echec_et_mat_simple(self):
        """Test la détection d'un échec et mat simple."""
        # Créer un mat du couloir
        self.jeu.plateau.grille = [[None for _ in range(8)] for _ in range(8)]
        
        roi_blanc = Roi('blanc', (7, 7))
        tour_noire1 = Tour('noir', (6, 0))
        tour_noire2 = Tour('noir', (7, 0))
        
        self.jeu.plateau.placer_piece(roi_blanc, (7, 7))
        self.jeu.plateau.placer_piece(tour_noire1, (6, 0))
        self.jeu.plateau.placer_piece(tour_noire2, (7, 0))
        
        # Le roi blanc ne peut pas bouger car toutes les cases sont attaquées
        self.assertTrue(self.jeu.est_echec_et_mat('blanc'))
    
    def test_est_pat_simple(self):
        """Test la détection d'un pat."""
        # Créer une position de pat
        self.jeu.plateau.grille = [[None for _ in range(8)] for _ in range(8)]
        
        roi_blanc = Roi('blanc', (7, 7))
        reine_noire = Reine('noir', (6, 5))
        roi_noir = Roi('noir', (0, 0))
        
        self.jeu.plateau.placer_piece(roi_blanc, (7, 7))
        self.jeu.plateau.placer_piece(reine_noire, (6, 5))
        self.jeu.plateau.placer_piece(roi_noir, (0, 0))
        
        # Le roi blanc n'est pas en échec mais ne peut pas bouger
        self.assertFalse(self.jeu.est_echec('blanc'))
        self.assertTrue(self.jeu.est_pat('blanc'))
    
    def test_changer_joueur(self):
        """Test le changement de joueur."""
        self.assertEqual(self.jeu.joueur_actuel, self.jeu.joueur_blanc)
        
        self.jeu.changer_joueur()
        self.assertEqual(self.jeu.joueur_actuel, self.jeu.joueur_noir)
        
        self.jeu.changer_joueur()
        self.assertEqual(self.jeu.joueur_actuel, self.jeu.joueur_blanc)
    
    def test_effectuer_coup_invalide_pas_de_piece(self):
        """Test qu'on ne peut pas effectuer un coup s'il n'y a pas de pièce."""
        resultat = self.jeu.effectuer_coup((4, 4), (5, 4))
        self.assertFalse(resultat)
    
    def test_effectuer_coup_invalide_mauvaise_couleur(self):
        """Test qu'on ne peut pas déplacer une pièce adverse."""
        # C'est au tour des blancs, essayer de bouger une pièce noire
        resultat = self.jeu.effectuer_coup((1, 4), (2, 4))
        self.assertFalse(resultat)
    
    def test_effectuer_coup_valide_pion(self):
        """Test un coup valide de pion."""
        resultat = self.jeu.effectuer_coup((6, 4), (4, 4))
        self.assertTrue(resultat)
        
        # Vérifier que le pion a été déplacé
        piece = self.jeu.plateau.obtenir_piece((4, 4))
        self.assertIsInstance(piece, Pion)
        self.assertEqual(piece.couleur, 'blanc')
    
    def test_obtenir_tous_mouvements_legaux_position_initiale(self):
        """Test le calcul de tous les mouvements légaux en position initiale."""
        mouvements_blancs = self.jeu.obtenir_tous_mouvements_legaux('blanc')
        
        # En position initiale, les blancs ont 20 coups possibles
        # (16 coups de pions + 4 coups de cavaliers)
        self.assertEqual(len(mouvements_blancs), 20)
    
    def test_historique(self):
        """Test que l'historique des coups est enregistré."""
        self.assertEqual(len(self.jeu.historique), 0)
        
        self.jeu.effectuer_coup((6, 4), (4, 4))
        self.assertEqual(len(self.jeu.historique), 1)
        
        depart, arrivee, piece = self.jeu.historique[0]
        self.assertEqual(depart, (6, 4))
        self.assertEqual(arrivee, (4, 4))
        self.assertIsInstance(piece, Pion)
    
    def test_notation_vers_position(self):
        """Test la conversion de notation en position."""
        self.assertEqual(self.jeu._notation_vers_position('e2'), (6, 4))
        self.assertEqual(self.jeu._notation_vers_position('e4'), (4, 4))
        self.assertEqual(self.jeu._notation_vers_position('a1'), (7, 0))
        self.assertEqual(self.jeu._notation_vers_position('h8'), (0, 7))
    
    def test_coup_qui_met_roi_en_echec_refuse(self):
        """Test qu'un coup qui met son propre roi en échec est refusé."""
        # Créer une situation où déplacer un pion met le roi en échec
        self.jeu.plateau.grille = [[None for _ in range(8)] for _ in range(8)]
        
        roi_blanc = Roi('blanc', (7, 4))
        pion_blanc = Pion('blanc', (6, 4))
        tour_noire = Tour('noir', (0, 4))
        
        self.jeu.plateau.placer_piece(roi_blanc, (7, 4))
        self.jeu.plateau.placer_piece(pion_blanc, (6, 4))
        self.jeu.plateau.placer_piece(tour_noire, (0, 4))
        
        # Essayer de déplacer le pion qui protège le roi sur le côté (capture diagonale)
        # Ajouter un pion noir pour permettre une capture diagonale
        pion_noir = Pion('noir', (5, 5))
        self.jeu.plateau.placer_piece(pion_noir, (5, 5))
        
        self.jeu.joueur_actuel = self.jeu.joueur_blanc
        resultat = self.jeu.effectuer_coup((6, 4), (5, 5))
        
        # Le coup devrait être refusé car il met le roi en échec
        self.assertFalse(resultat)


if __name__ == '__main__':
    unittest.main()

"""
Tests unitaires pour les classes de pièces d'échecs.
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.piece import Pion, Tour, Cavalier, Fou, Reine, Roi
from src.plateau import Plateau


class TestPion(unittest.TestCase):
    """Tests pour la classe Pion."""
    
    def setUp(self):
        """Initialise un plateau vide avant chaque test."""
        self.plateau = Plateau()
    
    def test_mouvement_initial_deux_cases(self):
        """Test que le pion peut avancer de deux cases lors du premier mouvement."""
        pion = Pion('blanc', (6, 4))
        self.plateau.placer_piece(pion, (6, 4))
        
        mouvements = pion.mouvements_possibles(self.plateau)
        
        self.assertIn((5, 4), mouvements)
        self.assertIn((4, 4), mouvements)
    
    def test_mouvement_une_case(self):
        """Test que le pion avance d'une case après avoir bougé."""
        pion = Pion('blanc', (5, 4))
        pion.a_bouge = True
        self.plateau.placer_piece(pion, (5, 4))
        
        mouvements = pion.mouvements_possibles(self.plateau)
        
        self.assertIn((4, 4), mouvements)
        self.assertNotIn((3, 4), mouvements)
    
    def test_capture_diagonale(self):
        """Test que le pion peut capturer en diagonale."""
        pion_blanc = Pion('blanc', (5, 4))
        pion_noir = Pion('noir', (4, 5))
        
        self.plateau.placer_piece(pion_blanc, (5, 4))
        self.plateau.placer_piece(pion_noir, (4, 5))
        
        mouvements = pion_blanc.mouvements_possibles(self.plateau)
        
        self.assertIn((4, 5), mouvements)
    
    def test_symbole(self):
        """Test que le symbole du pion est correct."""
        pion_blanc = Pion('blanc', (6, 0))
        pion_noir = Pion('noir', (1, 0))
        
        self.assertEqual(pion_blanc.symbole(), '♙')
        self.assertEqual(pion_noir.symbole(), '♟')


class TestTour(unittest.TestCase):
    """Tests pour la classe Tour."""
    
    def setUp(self):
        """Initialise un plateau vide avant chaque test."""
        self.plateau = Plateau()
    
    def test_mouvement_horizontal(self):
        """Test que la tour peut se déplacer horizontalement."""
        tour = Tour('blanc', (4, 4))
        self.plateau.placer_piece(tour, (4, 4))
        
        mouvements = tour.mouvements_possibles(self.plateau)
        
        # Vérifier quelques positions horizontales
        self.assertIn((4, 0), mouvements)
        self.assertIn((4, 7), mouvements)
    
    def test_mouvement_vertical(self):
        """Test que la tour peut se déplacer verticalement."""
        tour = Tour('blanc', (4, 4))
        self.plateau.placer_piece(tour, (4, 4))
        
        mouvements = tour.mouvements_possibles(self.plateau)
        
        # Vérifier quelques positions verticales
        self.assertIn((0, 4), mouvements)
        self.assertIn((7, 4), mouvements)
    
    def test_blocage_par_piece(self):
        """Test que la tour est bloquée par une autre pièce."""
        tour = Tour('blanc', (4, 4))
        pion = Pion('blanc', (4, 6))
        
        self.plateau.placer_piece(tour, (4, 4))
        self.plateau.placer_piece(pion, (4, 6))
        
        mouvements = tour.mouvements_possibles(self.plateau)
        
        # La tour peut aller jusqu'à la case avant le pion
        self.assertIn((4, 5), mouvements)
        # Mais pas sur le pion ni au-delà
        self.assertNotIn((4, 6), mouvements)
        self.assertNotIn((4, 7), mouvements)


class TestCavalier(unittest.TestCase):
    """Tests pour la classe Cavalier."""
    
    def setUp(self):
        """Initialise un plateau vide avant chaque test."""
        self.plateau = Plateau()
    
    def test_mouvement_en_l(self):
        """Test que le cavalier se déplace en forme de L."""
        cavalier = Cavalier('blanc', (4, 4))
        self.plateau.placer_piece(cavalier, (4, 4))
        
        mouvements = cavalier.mouvements_possibles(self.plateau)
        
        # Vérifier les 8 positions possibles en L
        positions_attendues = [
            (2, 3), (2, 5), (3, 2), (3, 6),
            (5, 2), (5, 6), (6, 3), (6, 5)
        ]
        
        for pos in positions_attendues:
            self.assertIn(pos, mouvements)
    
    def test_peut_sauter_pieces(self):
        """Test que le cavalier peut sauter par-dessus d'autres pièces."""
        cavalier = Cavalier('blanc', (4, 4))
        pion = Pion('blanc', (3, 4))
        
        self.plateau.placer_piece(cavalier, (4, 4))
        self.plateau.placer_piece(pion, (3, 4))
        
        mouvements = cavalier.mouvements_possibles(self.plateau)
        
        # Le cavalier peut toujours atteindre ses positions malgré le pion
        self.assertIn((2, 3), mouvements)
        self.assertIn((2, 5), mouvements)


class TestFou(unittest.TestCase):
    """Tests pour la classe Fou."""
    
    def setUp(self):
        """Initialise un plateau vide avant chaque test."""
        self.plateau = Plateau()
    
    def test_mouvement_diagonal(self):
        """Test que le fou se déplace en diagonale."""
        fou = Fou('blanc', (4, 4))
        self.plateau.placer_piece(fou, (4, 4))
        
        mouvements = fou.mouvements_possibles(self.plateau)
        
        # Vérifier quelques positions diagonales
        self.assertIn((0, 0), mouvements)
        self.assertIn((7, 7), mouvements)
        self.assertIn((1, 7), mouvements)
        self.assertIn((7, 1), mouvements)


class TestReine(unittest.TestCase):
    """Tests pour la classe Reine."""
    
    def setUp(self):
        """Initialise un plateau vide avant chaque test."""
        self.plateau = Plateau()
    
    def test_mouvement_combine(self):
        """Test que la reine combine les mouvements de la tour et du fou."""
        reine = Reine('blanc', (4, 4))
        self.plateau.placer_piece(reine, (4, 4))
        
        mouvements = reine.mouvements_possibles(self.plateau)
        
        # Mouvements horizontaux et verticaux (comme une tour)
        self.assertIn((4, 0), mouvements)
        self.assertIn((0, 4), mouvements)
        
        # Mouvements diagonaux (comme un fou)
        self.assertIn((0, 0), mouvements)
        self.assertIn((7, 7), mouvements)


class TestRoi(unittest.TestCase):
    """Tests pour la classe Roi."""
    
    def setUp(self):
        """Initialise un plateau vide avant chaque test."""
        self.plateau = Plateau()
    
    def test_mouvement_une_case(self):
        """Test que le roi se déplace d'une case dans toutes les directions."""
        roi = Roi('blanc', (4, 4))
        self.plateau.placer_piece(roi, (4, 4))
        
        mouvements = roi.mouvements_possibles(self.plateau)
        
        # Vérifier les 8 cases adjacentes
        positions_attendues = [
            (3, 3), (3, 4), (3, 5),
            (4, 3),         (4, 5),
            (5, 3), (5, 4), (5, 5)
        ]
        
        for pos in positions_attendues:
            self.assertIn(pos, mouvements)
    
    def test_ne_peut_pas_bouger_deux_cases(self):
        """Test que le roi ne peut pas se déplacer de deux cases (sauf roque)."""
        roi = Roi('blanc', (4, 4))
        self.plateau.placer_piece(roi, (4, 4))
        
        mouvements = roi.mouvements_possibles(self.plateau)
        
        # Vérifier qu'il ne peut pas aller à deux cases
        self.assertNotIn((2, 4), mouvements)
        self.assertNotIn((6, 4), mouvements)


if __name__ == '__main__':
    unittest.main()

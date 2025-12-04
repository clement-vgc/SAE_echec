"""
Tests unitaires pour la classe Plateau.
"""

import unittest
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.plateau import Plateau
from src.piece import Pion, Tour, Cavalier, Fou, Reine, Roi


class TestPlateau(unittest.TestCase):
    """Tests pour la classe Plateau."""
    
    def setUp(self):
        """Initialise un plateau avant chaque test."""
        self.plateau = Plateau()
    
    def test_initialisation_plateau_vide(self):
        """Test que le plateau est vide à la création."""
        for ligne in range(8):
            for colonne in range(8):
                self.assertIsNone(self.plateau.grille[ligne][colonne])
    
    def test_initialisation_complete(self):
        """Test que l'initialisation place toutes les pièces correctement."""
        self.plateau.initialiser()
        
        # Vérifier les pions
        for col in range(8):
            self.assertIsInstance(self.plateau.grille[1][col], Pion)
            self.assertEqual(self.plateau.grille[1][col].couleur, 'noir')
            
            self.assertIsInstance(self.plateau.grille[6][col], Pion)
            self.assertEqual(self.plateau.grille[6][col].couleur, 'blanc')
        
        # Vérifier les tours blanches
        self.assertIsInstance(self.plateau.grille[7][0], Tour)
        self.assertIsInstance(self.plateau.grille[7][7], Tour)
        
        # Vérifier les rois
        self.assertIsInstance(self.plateau.grille[0][4], Roi)
        self.assertEqual(self.plateau.grille[0][4].couleur, 'noir')
        self.assertIsInstance(self.plateau.grille[7][4], Roi)
        self.assertEqual(self.plateau.grille[7][4].couleur, 'blanc')
    
    def test_obtenir_piece(self):
        """Test la récupération d'une pièce."""
        pion = Pion('blanc', (6, 4))
        self.plateau.placer_piece(pion, (6, 4))
        
        piece_recuperee = self.plateau.obtenir_piece((6, 4))
        
        self.assertEqual(piece_recuperee, pion)
        self.assertEqual(piece_recuperee.couleur, 'blanc')
    
    def test_placer_piece(self):
        """Test le placement d'une pièce."""
        pion = Pion('blanc', (6, 4))
        self.plateau.placer_piece(pion, (6, 4))
        
        self.assertEqual(self.plateau.grille[6][4], pion)
        self.assertEqual(pion.position, (6, 4))
    
    def test_retirer_piece(self):
        """Test le retrait d'une pièce."""
        pion = Pion('blanc', (6, 4))
        self.plateau.placer_piece(pion, (6, 4))
        
        piece_retiree = self.plateau.retirer_piece((6, 4))
        
        self.assertEqual(piece_retiree, pion)
        self.assertIsNone(self.plateau.grille[6][4])
    
    def test_deplacer_piece(self):
        """Test le déplacement d'une pièce."""
        pion = Pion('blanc', (6, 4))
        self.plateau.placer_piece(pion, (6, 4))
        
        self.plateau.deplacer_piece((6, 4), (5, 4))
        
        self.assertIsNone(self.plateau.grille[6][4])
        self.assertEqual(self.plateau.grille[5][4], pion)
        self.assertEqual(pion.position, (5, 4))
        self.assertTrue(pion.a_bouge)
    
    def test_deplacer_piece_avec_capture(self):
        """Test le déplacement avec capture d'une pièce adverse."""
        pion_blanc = Pion('blanc', (5, 4))
        pion_noir = Pion('noir', (4, 4))
        
        self.plateau.placer_piece(pion_blanc, (5, 4))
        self.plateau.placer_piece(pion_noir, (4, 4))
        
        piece_capturee = self.plateau.deplacer_piece((5, 4), (4, 4))
        
        self.assertEqual(piece_capturee, pion_noir)
        self.assertIn(pion_noir, self.plateau.pieces_capturees)
        self.assertEqual(self.plateau.grille[4][4], pion_blanc)
    
    def test_est_case_vide(self):
        """Test la vérification de case vide."""
        self.assertTrue(self.plateau.est_case_vide((4, 4)))
        
        pion = Pion('blanc', (4, 4))
        self.plateau.placer_piece(pion, (4, 4))
        
        self.assertFalse(self.plateau.est_case_vide((4, 4)))
    
    def test_est_position_valide(self):
        """Test la validation de position."""
        self.assertTrue(self.plateau.est_position_valide((0, 0)))
        self.assertTrue(self.plateau.est_position_valide((7, 7)))
        self.assertTrue(self.plateau.est_position_valide((4, 4)))
        
        self.assertFalse(self.plateau.est_position_valide((-1, 0)))
        self.assertFalse(self.plateau.est_position_valide((0, -1)))
        self.assertFalse(self.plateau.est_position_valide((8, 0)))
        self.assertFalse(self.plateau.est_position_valide((0, 8)))
    
    def test_trouver_roi(self):
        """Test la recherche du roi."""
        self.plateau.initialiser()
        
        position_roi_blanc = self.plateau.trouver_roi('blanc')
        position_roi_noir = self.plateau.trouver_roi('noir')
        
        self.assertEqual(position_roi_blanc, (7, 4))
        self.assertEqual(position_roi_noir, (0, 4))
    
    def test_obtenir_toutes_pieces(self):
        """Test la récupération de toutes les pièces d'une couleur."""
        self.plateau.initialiser()
        
        pieces_blanches = self.plateau.obtenir_toutes_pieces('blanc')
        pieces_noires = self.plateau.obtenir_toutes_pieces('noir')
        
        self.assertEqual(len(pieces_blanches), 16)
        self.assertEqual(len(pieces_noires), 16)
        
        # Vérifier que toutes les pièces ont la bonne couleur
        for piece in pieces_blanches:
            self.assertEqual(piece.couleur, 'blanc')
        
        for piece in pieces_noires:
            self.assertEqual(piece.couleur, 'noir')
    
    def test_copier_plateau(self):
        """Test la copie du plateau."""
        self.plateau.initialiser()
        
        copie = self.plateau.copier()
        
        # Vérifier que c'est une copie et non la même instance
        self.assertIsNot(copie, self.plateau)
        
        # Vérifier que le contenu est identique
        for ligne in range(8):
            for colonne in range(8):
                piece_originale = self.plateau.grille[ligne][colonne]
                piece_copiee = copie.grille[ligne][colonne]
                
                if piece_originale is None:
                    self.assertIsNone(piece_copiee)
                else:
                    self.assertIsInstance(piece_copiee, type(piece_originale))
                    self.assertEqual(piece_copiee.couleur, piece_originale.couleur)
                    self.assertEqual(piece_copiee.position, piece_originale.position)


if __name__ == '__main__':
    unittest.main()

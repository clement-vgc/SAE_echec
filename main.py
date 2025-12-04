#!/usr/bin/env python3
"""
Point d'entrée principal pour le jeu d'échecs.
Lance une partie d'échecs dans le terminal pour deux joueurs locaux.
"""

from src.jeu import Jeu


def main():
    """Fonction principale qui lance le jeu."""
    print("\n")
    print("╔══════════════════════════════════════════════════╗")
    print("║        JEU D'ÉCHECS - VERSION TERMINALE          ║")
    print("╚══════════════════════════════════════════════════╝")
    print("\n")
    
    # Demander les noms des joueurs
    nom_joueur1 = input("Nom du joueur 1 (blancs) [Joueur 1]: ").strip()
    if not nom_joueur1:
        nom_joueur1 = "Joueur 1"
    
    nom_joueur2 = input("Nom du joueur 2 (noirs) [Joueur 2]: ").strip()
    if not nom_joueur2:
        nom_joueur2 = "Joueur 2"
    
    # Créer et démarrer le jeu
    jeu = Jeu(nom_joueur1, nom_joueur2)
    jeu.demarrer()


if __name__ == "__main__":
    main()

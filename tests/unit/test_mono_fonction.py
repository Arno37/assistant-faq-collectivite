import pytest
import sys
import os

# Ajout du dossier racine au chemin de recherche de Python pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.nettoyage import nettoyer_texte

def test_unitaire_nettoyage_simple():
    """
    Test unitaire ultra-simple sur la fonction nettoyer_texte.
    On vérifie qu'une chaîne en MAJUSCULES devient des minuscules.
    """
    # 1. Donnée de départ
    entree = "MAIRIE"
    print(f"\n[UNIT TEST] Entrée : {entree}")
    
    # 2. On applique la fonction
    resultat = nettoyer_texte(entree)
    print(f"[UNIT TEST] Sortie : {resultat}")
    
    # 3. On vérifie que le résultat est bien celui attendu
    assert resultat == "mairie"

if __name__ == "__main__":
    import pytest
    # On lance pytest sur ce fichier uniquement avec l'affichage des prints (-s)
    pytest.main([__file__, "-s"])

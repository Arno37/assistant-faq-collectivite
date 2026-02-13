import os
import shutil
import sys

# Ajout du dossier racine au chemin de recherche de Python pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.chargement_donnees import charger_documents
from src.utils.nettoyage import nettoyer_texte

def test_integration_chaine_chargement_nettoyage():
    """
    Test d'intégration simple :
    Vérifie que la fonction 'charger_documents' et la fonction 'nettoyer_texte'
    travaillent bien ensemble.
    """
    # 1. PRÉPARATION : On crée un dossier et un fichier réel
    dossier_test = "temp_integration_test"
    os.makedirs(dossier_test, exist_ok=True)
    
    chemin_fichier = os.path.join(dossier_test, "test.txt")
    with open(chemin_fichier, "w", encoding="utf-8") as f:
        f.write("MAIRIE : OUVERT À 9H")

    try:
        # 2. ÉTAPE 1 : On utilise la première fonction (Chargement)
        docs = charger_documents(dossier_test)
        # On récupère le texte brut du premier fichier chargé
        texte_brut = docs[0] 
        print(f"\n[DEBUG] Texte lu dans le fichier :\n{texte_brut}")

        # 3. ÉTAPE 2 : On passe ce résultat à la deuxième fonction (Nettoyage)
        texte_final = nettoyer_texte(texte_brut)
        print(f"\n[DEBUG] Texte après nettoyage (en mémoire) :\n{texte_final}")

        # 4. VÉRIFICATION : Est-ce que la chaîne a fonctionné ?
        # Les majuscules doivent être en minuscules et les accents supprimés
        assert "mairie" in texte_final
        assert "ouvert a 9h" in texte_final
        
        print("\n✅ Intégration réussie : Le texte a été chargé ET nettoyé.")

    finally:
        # 5. NETTOYAGE : Désactivé pour que vous puissiez voir le fichier !
        # if os.path.exists(dossier_test):
        #     shutil.rmtree(dossier_test)
        print(f"\n📂 Le dossier de test est toujours là : {os.path.abspath(dossier_test)}")

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-s"])

import sys
import os

# Ajout du root du projet au sys.path pour les imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.benchmark.run_benchmark import calculer_score_keywords
from src.outils.nettoyage import nettoyer_texte

def test_nettoyer_texte_accents():
    """Vérifie que les accents sont bien supprimés"""
    entree = "Éléphant à la déchèterie"
    attendu = "elephant a la decheterie"
    assert nettoyer_texte(entree) == attendu

def test_nettoyer_texte_minuscule():
    """Vérifie le passage en minuscules et espaces"""
    entree = "  VÉRIFICATION  DU   TEXTE "
    attendu = "verification du texte"
    assert nettoyer_texte(entree) == attendu

def test_calculer_score_keywords_parfait():
    """Vérifie que si tous les mots sont là, le score est 100"""
    reponse = "Il faut aller en mairie avec une pièce d'identité."
    keywords = ["mairie", "identité"]
    score = calculer_score_keywords(reponse, keywords)
    assert score == 100

def test_calculer_score_keywords_partiel():
    """Vérifie un score de 50%"""
    reponse = "C'est à la mairie."
    keywords = ["mairie", "gratuit"] # 'mairie' est là, 'gratuit' non
    score = calculer_score_keywords(reponse, keywords)
    assert score == 50

def test_calculer_score_keywords_vide():
    """Vérifie si pas de mots-clés attendus (doit retourner 100 par convention)"""
    reponse = "Bonjour"
    keywords = []
    score = calculer_score_keywords(reponse, keywords)
    assert score == 100

def test_calculer_score_keywords_insensible_casse():
    """Vérifie que la comparaison ignore la casse"""
    reponse = "MAIRIE"
    keywords = ["mairie"]
    score = calculer_score_keywords(reponse, keywords)
    assert score == 100

import pytest
import os
import json
import sys

# Ajout du dossier racine au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.strategies.strategie_b_rag import interroger_rag

def charger_golden_set():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw/golden_set.json"))
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['golden_set']

def calculer_score_keywords(reponse, expected_keywords):
    if not expected_keywords:
        return 100
    reponse_lower = reponse.lower()
    found = sum(1 for kw in expected_keywords if kw.lower() in reponse_lower)
    return (found / len(expected_keywords)) * 100

@pytest.mark.parametrize("test_case", charger_golden_set())
def test_non_regression_golden_set(test_case):
    """
    Test de non-régression : 
    Vérifie que la Stratégie B (RAG) maintient un niveau de performance acceptable
    sur les questions du Golden Set.
    """
    question = test_case['question']
    expected_keywords = test_case.get('expected_keywords', [])
    
    # On n'exécute le test que pour les questions de type 'direct_match' ou 'reformulation'
    # car les 'hors_sujet' ont un comportement différent.
    if test_case['type'] in ['direct_match', 'reformulation']:
        reponse = interroger_rag(question)
        score = calculer_score_keywords(reponse, expected_keywords)
        
        # Seuil de succès : On veut au moins 40% des mots-clés pour valider la non-régression
        # (C'est un seuil minimal pour éviter les faux négatifs en CI)
        assert score >= 40, f"Score trop bas ({score}%) pour la question : {question}"
    
    elif test_case['type'] == 'hors_sujet':
        reponse = interroger_rag(question)
        # Pour un hors-sujet, on vérifie l'aveu d'ignorance poli
        assert "Bonjour" in reponse
        assert "domaine de compétence" in reponse or "pas habilité" in reponse

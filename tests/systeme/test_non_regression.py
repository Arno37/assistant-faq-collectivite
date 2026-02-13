import pytest
import os
import json
import sys
import time

# Ajout du dossier racine au path Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.strategies.strategie_b_rag import interroger_rag

def charger_golden_set():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/raw/golden_set.json"))
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['golden_set']
    
    # SECURITÉ CI/CD : En environnement GitHub Actions, on ne teste que 
    # les questions "direct_match" et "hors_sujet" (les plus fiables).
    # Les questions "complexe" et "reformulation" sont testées en local uniquement
    # car elles nécessitent plus de contexte et sont sensibles aux quotas API.
    if os.getenv("GITHUB_ACTIONS") == "true":
        import random
        questions_ci = [q for q in questions if q['type'] in ['direct_match', 'hors_sujet']]
        print(f"\n⚠️ CI détecté : {len(questions_ci)} questions fiables sélectionnées (direct_match + hors_sujet).")
        return random.sample(questions_ci, min(5, len(questions_ci)))
    
    return questions

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
    Vérifie que la Stratégie B (RAG) maintient un niveau de performance acceptable.
    """
    # Pause pour ne pas saturer l'API gratuite (3s pour être sûr)
    time.sleep(3 if os.getenv("GITHUB_ACTIONS") == "true" else 2.0)

    question = test_case['question']
    expected_keywords = test_case.get('expected_keywords', [])
    
    reponse = interroger_rag(question)

    # DETECTION DE SATURATION API
    if "difficulté technique" in reponse:
         pytest.skip("API Hugging Face saturée (Quota). Test ignoré pour ne pas fausser les résultats.")

    if test_case['type'] in ['direct_match', 'reformulation', 'complexe']:
        score = calculer_score_keywords(reponse, expected_keywords)
        assert score >= 40, f"Score trop bas ({score}%) pour la question : {question}"
    
    elif test_case['type'] == 'hors_sujet':
        assert "Bonjour" in reponse
        assert "domaine de compétence" in reponse or "pas habilité" in reponse

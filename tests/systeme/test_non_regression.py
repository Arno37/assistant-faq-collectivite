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
    
    # SECURITÉ CI/CD : Si on est sur GitHub Actions, on ne teste que 5 questions
    # pour éviter de saturer le quota gratuit de l'API Hugging Face
    if os.getenv("GITHUB_ACTIONS") == "true":
        import random
        print("\n⚠️ Environnement CI détecté : Échantillonnage de 5 questions pour préserver le quota.")
        return random.sample(questions, 5)
    
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
    # Pause pour ne pas saturer l'API gratuite
    time.sleep(2 if os.getenv("GITHUB_ACTIONS") == "true" else 0.5)

    question = test_case['question']
    expected_keywords = test_case.get('expected_keywords', [])
    
    if test_case['type'] in ['direct_match', 'reformulation']:
        reponse = interroger_rag(question)
        score = calculer_score_keywords(reponse, expected_keywords)
        # Seuil à 40% pour être tolérant en CI tout en gardant une mesure de qualité
        assert score >= 40, f"Score trop bas ({score}%) pour la question : {question}"
    
    elif test_case['type'] == 'hors_sujet':
        reponse = interroger_rag(question)
        assert "Bonjour" in reponse
        assert "domaine de compétence" in reponse or "pas habilité" in reponse

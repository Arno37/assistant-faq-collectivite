import sys
import os
import pytest

# Ajout du root du projet au sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.benchmark.run_benchmark import charger_golden_set, calculer_score_keywords
from src.strategies.strategie_b_rag import interroger_rag

def test_performance_rag_golden_set():
    """
    Test de non-régression : Vérifie que la Stratégie B (RAG) 
    maintient un niveau de performance acceptable sur le Golden Set.
    """
    print("\n🚀 Lancement du test de non-régression (Stratégie B)...")
    
    # 1. Charger le Golden Set
    golden_set = charger_golden_set()
    
    # On se concentre sur les questions de type 'direct_match' pour le test de CI
    # pour éviter de tout faire tourner (gain de temps)
    questions_test = [q for q in golden_set if q['type'] == 'direct_match']
    
    scores = []
    
    # 2. Exécuter la stratégie sur ce sous-ensemble
    for item in questions_test:
        question = item['question']
        expected_keywords = item.get('expected_keywords', [])
        
        try:
            reponse = interroger_rag(question)
            score = calculer_score_keywords(reponse, expected_keywords)
            scores.append(score)
            print(f"   ✅ Question: {item['id']} | Score: {score}%")
        except Exception as e:
            print(f"   ❌ Question: {item['id']} | Erreur: {e}")
            scores.append(0)

    # 3. Calculer la moyenne
    score_moyen = sum(scores) / len(scores) if scores else 0
    print(f"\n📊 Score moyen sur le Golden Set (Direct Match) : {score_moyen:.1f}%")

    # 4. ASSERT : On exige au moins 55% de réussite sur les correspondances directes
    # (C'est notre seuil de non-régression)
    assert score_moyen >= 55, f"Régression détectée ! Le score moyen ({score_moyen}%) est inférieur au seuil de 55%."

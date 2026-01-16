import sys
import os
import json
import time
from datetime import datetime

# Permet d'importer les modules src.*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.strategies.strategie_a_llm_seul import executer_strategie_a
from src.strategies.strategie_b_rag import interroger_rag
from src.strategies.strategie_c_extractif import interroger_extractif

# Chemins des fichiers
GOLDEN_SET_PATH = os.path.join(os.path.dirname(__file__), "../../data/raw/golden_set.json")
OUTPUT_JSON_PATH = os.path.join(os.path.dirname(__file__), "../../docs/benchmark/resultats_benchmark.json")
OUTPUT_CSV_PATH = os.path.join(os.path.dirname(__file__), "../../docs/benchmark/resultats_benchmark.csv")

def charger_golden_set():
    """Charge le Golden Set depuis le fichier JSON"""
    with open(GOLDEN_SET_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['golden_set']

def calculer_score_keywords(reponse, expected_keywords):
    """Calcule le pourcentage de mots-clés trouvés dans la réponse"""
    if not expected_keywords:
        return 100  # Si pas de mots-clés attendus, score parfait
    
    reponse_lower = reponse.lower()
    keywords_found = sum(1 for kw in expected_keywords if kw.lower() in reponse_lower)
    return int((keywords_found / len(expected_keywords)) * 100)

def tester_strategie(strategie_func, question, strategie_name):
    """Teste une stratégie et mesure la latence"""
    print(f"  Testing {strategie_name}...", end=" ")
    
    try:
        start_time = time.time()
        reponse = strategie_func(question)
        latency_ms = int((time.time() - start_time) * 1000)
        
        print(f"✅ ({latency_ms}ms)")
        
        return {
            "response": reponse,
            "latency_ms": latency_ms,
            "error": None
        }
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            "response": "",
            "latency_ms": 0,
            "error": str(e)
        }

def run_benchmark():
    """Exécute le benchmark complet"""
    print("="*60)
    print("🚀 BENCHMARK DES STRATÉGIES FAQ")
    print("="*60)
    
    # Charger le Golden Set
    print("\n📚 Chargement du Golden Set...")
    golden_set = charger_golden_set()
    print(f"✅ {len(golden_set)} questions chargées\n")
    
    # Résultats
    results = []
    
    # Statistiques globales
    stats = {
        "A": {"scores": [], "latencies": [], "errors": 0},
        "B": {"scores": [], "latencies": [], "errors": 0},
        "C": {"scores": [], "latencies": [], "errors": 0}
    }
    
    # Tester chaque question
    for i, item in enumerate(golden_set, 1):
        print(f"\n[{i}/{len(golden_set)}] {item['question']}")
        
        question = item['question']
        expected_keywords = item.get('expected_keywords', [])
        
        # Tester les 3 stratégies
        result_a = tester_strategie(executer_strategie_a, question, "Stratégie A")
        result_b = tester_strategie(interroger_rag, question, "Stratégie B")
        result_c = tester_strategie(interroger_extractif, question, "Stratégie C")
        
        # Calculer les scores
        score_a = calculer_score_keywords(result_a['response'], expected_keywords) if not result_a['error'] else 0
        score_b = calculer_score_keywords(result_b['response'], expected_keywords) if not result_b['error'] else 0
        score_c = calculer_score_keywords(result_c['response'], expected_keywords) if not result_c['error'] else 0
        
        # Sauvegarder les résultats
        results.append({
            "question_id": item['id'],
            "question": question,
            "type": item.get('type', 'unknown'),
            "expected_keywords": expected_keywords,
            "strategies": {
                "A": {
                    "response": result_a['response'],
                    "latency_ms": result_a['latency_ms'],
                    "keywords_found": sum(1 for kw in expected_keywords if kw.lower() in result_a['response'].lower()),
                    "keywords_total": len(expected_keywords),
                    "score": score_a,
                    "error": result_a['error']
                },
                "B": {
                    "response": result_b['response'],
                    "latency_ms": result_b['latency_ms'],
                    "keywords_found": sum(1 for kw in expected_keywords if kw.lower() in result_b['response'].lower()),
                    "keywords_total": len(expected_keywords),
                    "score": score_b,
                    "error": result_b['error']
                },
                "C": {
                    "response": result_c['response'],
                    "latency_ms": result_c['latency_ms'],
                    "keywords_found": sum(1 for kw in expected_keywords if kw.lower() in result_c['response'].lower()),
                    "keywords_total": len(expected_keywords),
                    "score": score_c,
                    "error": result_c['error']
                }
            }
        })
        
        # Mettre à jour les stats
        if not result_a['error']:
            stats["A"]["scores"].append(score_a)
            stats["A"]["latencies"].append(result_a['latency_ms'])
        else:
            stats["A"]["errors"] += 1
            
        if not result_b['error']:
            stats["B"]["scores"].append(score_b)
            stats["B"]["latencies"].append(result_b['latency_ms'])
        else:
            stats["B"]["errors"] += 1
            
        if not result_c['error']:
            stats["C"]["scores"].append(score_c)
            stats["C"]["latencies"].append(result_c['latency_ms'])
        else:
            stats["C"]["errors"] += 1
    
    # Calculer les moyennes
    summary = {}
    for strat in ["A", "B", "C"]:
        scores = stats[strat]["scores"]
        latencies = stats[strat]["latencies"]
        
        summary[f"strategy_{strat}"] = {
            "avg_score": int(sum(scores) / len(scores)) if scores else 0,
            "avg_latency_ms": int(sum(latencies) / len(latencies)) if latencies else 0,
            "errors": stats[strat]["errors"],
            "total_tests": len(golden_set)
        }
    
    # Créer le fichier de résultats JSON
    output_data = {
        "metadata": {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": len(golden_set),
            "strategies_tested": ["A", "B", "C"]
        },
        "results": results,
        "summary": summary
    }
    
    # Sauvegarder JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)
    with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Résultats JSON sauvegardés : {OUTPUT_JSON_PATH}")
    
    # Créer le fichier CSV
    with open(OUTPUT_CSV_PATH, 'w', encoding='utf-8') as f:
        f.write("Question ID,Question,Type,Stratégie A Score,Stratégie B Score,Stratégie C Score,Stratégie A Latence (ms),Stratégie B Latence (ms),Stratégie C Latence (ms)\n")
        for r in results:
            f.write(f"{r['question_id']},\"{r['question']}\",{r['type']},{r['strategies']['A']['score']},{r['strategies']['B']['score']},{r['strategies']['C']['score']},{r['strategies']['A']['latency_ms']},{r['strategies']['B']['latency_ms']},{r['strategies']['C']['latency_ms']}\n")
    
    print(f"✅ Résultats CSV sauvegardés : {OUTPUT_CSV_PATH}")
    
    # Afficher le résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES RÉSULTATS")
    print("="*60)
    for strat in ["A", "B", "C"]:
        s = summary[f"strategy_{strat}"]
        print(f"\nStratégie {strat}:")
        print(f"  Score moyen     : {s['avg_score']}/100")
        print(f"  Latence moyenne : {s['avg_latency_ms']}ms")
        print(f"  Erreurs         : {s['errors']}/{s['total_tests']}")
    
    print("\n" + "="*60)
    print("✅ Benchmark terminé !")
    print("="*60)

if __name__ == "__main__":
    run_benchmark()

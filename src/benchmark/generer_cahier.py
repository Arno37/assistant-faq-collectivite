import json
import os

# Chemins
INPUT_JSON = "../../docs/benchmark/resultats_benchmark.json"
OUTPUT_MD = "../../docs/benchmark/CAHIER_CORRECTION.md"

def generer_cahier():
    if not os.path.exists(INPUT_JSON):
        print("Erreur : Le fichier de résultats n'existe pas.")
        return

    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# 📝 Cahier de Correction - Benchmark FAQ\n\n")
        f.write("Ce document sert à évaluer manuellement la **Stratégie B (RAG)**, qui est la plus performante.\n\n")
        f.write("## 💡 Barème de notation\n")
        f.write("- **Pertinence (0-2)** : 0=Inutile, 1=Incomplet, 2=Parfait\n")
        f.write("- **Hallucination (O/N)** : L'IA a-t-elle inventé une information ?\n\n")
        f.write("| ID | Question | Réponse Stratégie B | Score Mots-Clés | Pertinence (0-2) | Hallucination (O/N) |\n")
        f.write("|----|----------|---------------------|-----------------|------------------|---------------------|\n")

        for res in data['results']:
            q_id = res['question_id']
            question = res['question']
            resp_b = res['strategies']['B']['response'].replace("\n", " ")[:150] + "..."
            score_kw = res['strategies']['B']['score']
            
            f.write(f"| {q_id} | {question} | {resp_b} | {score_kw}/100 | [ ] | [ ] |\n")

    print(f"✅ Cahier de correction généré : {OUTPUT_MD}")

if __name__ == "__main__":
    generer_cahier()

# 📊 Grille d'Évaluation du Benchmark

Ce document sert à noter les performances de ton assistant intelligent.
Pour chaque question du "Golden Set" (tes 25 questions de test), tu devras tester les 3 stratégies et noter leur réponse.

## 🎯 Critères de Notation (Score sur 5)

| Note | Signification | Description |
| :--: | :------------ | :---------- |
| **5** | **Excellent** | Réponse exacte, complète et naturelle. |
| **4** | **Bon** | Réponse correcte mais on aurait pu faire mieux (style, détail). |
| **3** | **Moyen** | Réponse partiellement correcte ou un peu vague. |
| **2** | **Insuffisant** | Réponse hors sujet, incomplète ou formatage cassé. |
| **1** | **Hallucination** | L'IA invente des informations fausses (Très grave !). |

---

## 📝 Tes Résultats

| ID | Question (Exemples) | Stratégie A (LLM Seul) | Stratégie B (RAG) | Stratégie C (Extractif) |
|:--:|:------------------- |:----------------------:|:-----------------:|:-----------------------:|
| **1** | Quel est le Maire ? | Note : _/5 | Note : _/5 | Note : _/5 |
| **2** | Horaires de la piscine ? | Note : _/5 | Note : _/5 | Note : _/5 |
| **3** | Aides au logement ? | Note : _/5 | Note : _/5 | Note : _/5 |
| **4** | ... | ... | ... | ... |
| **5** | ... | ... | ... | ... |
| **...**| ... | ... | ... | ... |

### Comment procéder ?
1.  Prends une question (ex: "Quel est le Maire ?").
2.  Lance ton script `strategie_a_llm_seul.py` avec cette question.
3.  Lis la réponse et mets une note dans la colonne "Stratégie A".
4.  Fais pareil avec les autres stratégies quand elles seront prêtes.

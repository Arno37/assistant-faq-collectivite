# Rapport de Choix Stratégique : Assistant FAQ Intelligent

## 1. Introduction
L'objectif de ce projet est de doter la collectivité d'un assistant capable de répondre aux questions des administrés avec une fiabilité totale, tout en restant capable de comprendre le langage naturel. Après évaluation, la **Stratégie B (RAG - Retrieval Augmented Generation)** a été sélectionnée.

## 2. La Stratégie Choisie : Le RAG (Stratégie B)
Le RAG est une architecture qui connecte un Modèle de Langage (LLM) à une base de connaissances locale (nos fichiers de mairie).

### Pourquoi cette stratégie est supérieure ?
*   **Fiabilité (Anti-Hallucination) :** L'IA est contrainte de répondre uniquement à partir des documents fournis. Elle ne peut pas "inventer" des horaires ou des procédures.
*   **Intelligence Sémantique :** Grâce aux *Embeddings*, le système comprend que "déchetterie" et "recyclage des encombrants" sont liés, même si le mot exact n'est pas dans la question.
*   **Maintenance Simplifiée :** Pour mettre à jour l'assistant, il suffit de modifier un fichier texte ou JSON. Aucune modification de code ou ré-entraînement de l'IA n'est nécessaire.

## 3. Justification Technique
Le projet s'appuie sur des composants de pointe :
*   **Modèle d'Embeddings :** `all-MiniLM-L6-v2` pour transformer les textes en vecteurs mathématiques comparables.
*   **Modèle de Génération :** `Qwen2.5-7B-Instruct` (via Hugging Face) pour formuler des réponses humaines et polies.
*   **Contrôle de Contexte :** Un prompt système strict qui interdit à l'IA de sortir des données de la mairie.

## 4. Preuves de Fiabilité (Tests)
La robustesse du système est garantie par une suite de tests automatisés :

### A. Validation Unitaire (Input)
*   **Fichier :** `tests/unit/test_mono_fonction.py`
*   **Rôle :** Vérifie que toutes les entrées sont nettoyées (minuscules, suppression des accents).
*   **Résultat :** Garanti que les erreurs de frappe de l'administré n'empêchent pas la recherche de fonctionner.

### B. Validation d'Intégration (Pipeline)
*   **Fichier :** `tests/integration/test_chaine_complete.py`
*   **Rôle :** Vérifie la chaîne complète de "Lecture fichier -> Chargement -> Nettoyage".
*   **Résultat :** Prouve que le système est capable de lire physiquement des documents sur le serveur et de les transformer en données exploitables par l'IA.

## 5. Conclusion
La Stratégie B (RAG) est la solution la plus sûre et la plus évolutive pour une collectivité territoriale. Elle allie la **rigueur administrative** (source vérifiée) à la **modernité numérique** (interface conversationnelle intelligente).

---
*Date : 13/02/2026*  
*Rapport généré dans le cadre du projet : Assistant FAQ Intelligent pour Collectivité Territoriale*

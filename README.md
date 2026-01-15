# Assistant FAQ Intelligent pour Collectivité Territoriale

## 📋 Description

Projet de développement et d'évaluation de **3 stratégies d'intelligence artificielle** pour répondre automatiquement aux questions fréquentes des citoyens d'une communauté de communes.

### Les 3 Stratégies

| Stratégie | Description | Avantages | Inconvénients |
|-----------|-------------|-----------|---------------|
| **A - LLM Seul** | Utilise uniquement Llama 3 avec un prompt système | Simple, rapide | Risque d'hallucinations |
| **B - RAG** | Recherche sémantique + génération (Embeddings + LLM) | Fiable, sourcé | Plus complexe, latence |
| **C - Extractif** | Extraction de réponse exacte (Roberta-base-squad2) | Précis, pas d'hallucination | Rigide, moins naturel |

---

## 🚀 Installation

### Prérequis

- **Python 3.9+**
- Compte **Hugging Face** (gratuit) avec token API
- Connexion Internet (pour télécharger les modèles)

### Étapes

1. **Cloner le projet** (ou télécharger le dossier)

2. **Installer les dépendances**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configurer le token Hugging Face**
   
   Créez un fichier `.env` à la racine du projet :
   ```
   HF_TOKEN=votre_token_ici
   ```
   
   Pour obtenir votre token : [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## 📂 Structure du Projet

```
.
├── README.md                    # Ce fichier
├── requirements.txt             # Dépendances Python
├── .env                         # Token API (à créer)
│
├── data/
│   └── raw/
│       ├── faq_base.json       # Base de 70 questions-réponses
│       └── golden_set.json     # 30 questions de test pour benchmark
│
├── docs/                        # Documentation du projet
│   ├── benchmark/               # Grilles d'évaluation
│   │   ├── GRILLE_EVALUATION.md
│   │   └── GRILLE_EVALUATION.pdf
│   │
│   ├── day_1/                   # Livrables Jour 1
│   │   ├── note_de_cadrage.html
│   │   ├── note_de_cadrage.pdf
│   │   ├── rapport_veille_technique.html
│   │   └── rapport_veille_technique.pdf
│   │
│   └── day_2/                   # Livrables Jour 2
│       ├── protocole_benchmark.html
│       ├── protocole_benchmark.pdf
│       ├── grille_evaluation.html
│       └── grille_evaluation.pdf
│
└── src/
    ├── outils/
    │   ├── client_ia.py        # Configuration client Hugging Face
    │   └── chargement_donnees.py
    │
    └── strategies/
        ├── strategie_a_llm_seul.py    # Stratégie A
        ├── strategie_b_rag.py         # Stratégie B (RAG)
        └── strategie_c_extractif.py   # Stratégie C (à venir)
```

---

## 🎯 Utilisation

### Tester la Stratégie A (LLM Seul)

```bash
cd src/strategies
python3 strategie_a_llm_seul.py
```

**Exemple de sortie :**
```
--- Stratégie A : LLM Seul (meta-llama/Meta-Llama-3-8B-Instruct) ---
Question : quel âge as-tu ?
Réponse : Je ne suis pas habilité à répondre à ce genre de question.
```

### Tester la Stratégie B (RAG)

```bash
cd src/strategies
python3 strategie_b_rag.py
```

**Exemple de sortie :**
```
Chargement du modèle sémantique...
📚 70 documents chargés depuis la FAQ

Recherche pour : Je veux changer de prénom, comment faire ?
Document trouvé (Pertinence: 0.7823) : Question: Comment changer de prénom ? Réponse: Depuis 2017...
Réponse IA : Pour changer votre prénom, vous devez justifier d'un intérêt légitime...
```

### Modifier la question de test

Éditez la dernière ligne du fichier Python :

```python
if __name__ == "__main__":
    q = "Votre question ici"
    print("Réponse IA :", interroger_rag(q))
```

---

## 🐳 Utilisation avec Docker

### Prérequis Docker

- **Docker** installé ([Installation](https://docs.docker.com/get-docker/))
- **Docker Compose** installé (inclus avec Docker Desktop)

### Lancer le projet avec Docker

1. **Créer le fichier `.env`** avec ton token Hugging Face :
   ```
   HF_TOKEN=votre_token_ici
   ```

2. **Construire et lancer le conteneur** :
   ```bash
   docker-compose up --build
   ```

3. **Arrêter le conteneur** :
   ```bash
   docker-compose down
   ```

### Commandes Docker utiles

```bash
# Lancer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Exécuter une commande dans le conteneur
docker-compose exec faq-assistant python -m src.strategies.strategie_a_llm_seul

# Reconstruire l'image
docker-compose build --no-cache
```

---

## 📊 Données

### `faq_base.json`

Base de connaissance de **70 questions-réponses** organisées par catégories :
- État civil (mariages, naissances, décès)
- Urbanisme (permis de construire, déclarations)
- Déchets et environnement
- Transports
- Petite enfance
- Social et solidarité
- Vie associative
- Élections
- Logement
- Culture et sport
- Fiscalité
- Eau et assainissement

### `golden_set.json`

Jeu de test de **30 questions** pour évaluer les stratégies :
- 10 questions directes (match exact avec la FAQ)
- 10 reformulations (même sens, mots différents)
- 5 questions hors sujet (test des garde-fous)
- 5 questions complexes (nécessitant plusieurs réponses)

---

## 🧪 Benchmark

Le protocole d'évaluation compare les 3 stratégies sur :

| Critère | Poids | Description |
|---------|-------|-------------|
| **Exactitude** | 40% | La réponse contient les informations clés |
| **Pertinence** | 30% | La réponse est utile pour l'usager |
| **Hallucinations** | 20% | Absence d'informations inventées |
| **Latence** | 10% | Temps de réponse |

Les résultats sont consignés dans `benchmark/GRILLE_EVALUATION.pdf`.

---

## 🛠️ Technologies Utilisées

- **Python 3.9+**
- **Hugging Face Inference API** (accès aux modèles)
- **sentence-transformers** (embeddings sémantiques)
- **Meta-Llama-3-8B-Instruct** (génération de texte)
- **all-MiniLM-L6-v2** (embeddings, 384 dimensions)
- **roberta-base-squad2** (extraction de réponse)

---

## 📖 Documentation

- **Présentation stratégique** : `docs/day_1/note_de_cadrage.pdf`
- **Rapport de veille technique** : `docs/day_1/rapport_veille_technique.pdf`
- **Protocole de benchmark** : `docs/day_2/protocole_benchmark.pdf`
- **Grille d'évaluation** : `docs/day_2/grille_evaluation.pdf`

---

## 👤 Auteur

**Arnaud Rambourg**  
Projet réalisé dans le cadre d'un stage en développement IA pour collectivités territoriales.

---

## 📝 Licence

Projet à usage pédagogique et démonstratif.

---

## 🆘 Dépannage

### Erreur "HF_TOKEN not found"
Vérifiez que le fichier `.env` existe à la racine et contient :
```
HF_TOKEN=hf_xxxxxxxxxxxxx
```

### Erreur "Model is loading"
Le modèle Mistral peut être indisponible sur l'API gratuite. Le projet utilise Llama 3 par défaut.

### Téléchargement lent des modèles
Au premier lancement, `sentence-transformers` télécharge ~90 MB. C'est normal et ne se produit qu'une fois.

---

## 🚀 Prochaines Étapes

- [ ] Implémenter la Stratégie C (Extractif)
- [ ] Créer le script de benchmark automatique
- [ ] Déployer l'assistant en production (API FastAPI)
- [ ] Interface utilisateur (Streamlit ou web)

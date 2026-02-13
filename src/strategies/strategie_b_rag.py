import sys
import os
import torch
from sentence_transformers import SentenceTransformer, util
import json 

# Permet d'importer les modules src.* même si on lance le script depuis un sous-dossier
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.utils.client_ia import obtenir_client_hf, MODELE_LLM
from src.utils.nettoyage import nettoyer_texte

# Variables globales pour le chargement paresseux
_embedder = None
_corpus_embeddings = None
_documents_faq = None
_client = None

def _charger_ressources():
    global _embedder, _corpus_embeddings, _documents_faq, _client
    if _client is not None:
        return

    print("🚀 Chargement des ressources pour la Stratégie B...")
    
    # 1. Chargement de la FAQ
    chemin_faq = os.path.join(os.path.dirname(__file__), "../../data/raw/faq_base.json")
    with open(chemin_faq, 'r', encoding='utf-8') as f:
        data = json.load(f)

    _documents_faq = [
        f"Question: {item['question']} Réponse: {item['answer']}" 
        for item in data['faq']
    ]

    # 2. Modèle d'embeddings
    _embedder = SentenceTransformer('all-MiniLM-L6-v2')
    _corpus_embeddings = _embedder.encode(_documents_faq, convert_to_tensor=True, show_progress_bar=False)

    # 3. Client IA
    _client = obtenir_client_hf()
    print("✅ Ressources Stratégie B prêtes")


def construire_prompt_rag(question, contexte):
    """
    Construit le prompt système pour le modèle RAG.
    Prend en entrée la question et une liste de documents (contexte).
    """
    # On combine les documents en un seul texte
    contexte_combine = "\n\n".join(contexte)
    
    return f"""
Tu es un assistant de mairie poli et serviable. Commence TOUJOURS ta réponse par "Bonjour,".
Utilise EXCLUSIVEMENT le contexte ci-dessous pour répondre. 
Si la réponse n'est pas dans le contexte, dis exactement : "Bonjour, ceci sort de mon domaine de compétence. Veuillez renouveler votre demande en lien avec la collectivité territoriale ou les démarches administratives."

CONTEXTE : 
{contexte_combine}
"""

def interroger_rag(question):
    _charger_ressources()
    
    # Nettoyage de la question pour la recherche
    question_propre = nettoyer_texte(question)
    print(f"\n[DEBUG] Question brute : {question}")
    print(f"[DEBUG] Question nettoyée : {question_propre}")
    
    # A. Recherche des 3 documents les plus pertinents
    query_embedding = _embedder.encode(question_propre, convert_to_tensor=True, show_progress_bar=False)
    hits = util.semantic_search(query_embedding, _corpus_embeddings, top_k=3)
    
    # Récupérer les 3 meilleurs documents
    top_docs = [_documents_faq[hit['corpus_id']] for hit in hits[0]]
    scores = [hit['score'] for hit in hits[0]]
    
    # --- AJOUT SÉCURITÉ : Seuil de pertinence ---
    # Si même le meilleur document a un score trop bas (< 0.35), 
    # on considère que c'est hors sujet sans même interroger l'IA.
    if scores[0] < 0.35:
        return "Bonjour, ceci sort de mon domaine de compétence. Veuillez renouveler votre demande en lien avec la collectivité territoriale ou les démarches administratives."
    # ---------------------------------------------

    print(f"\n📊 Top 3 documents trouvés :")
    for i, (doc, score) in enumerate(zip(top_docs, scores), 1):
        print(f"  {i}. Pertinence: {score:.4f} - {doc[:80]}...")
    
    # B. Construction de la réponse avec l'IA
    prompt_systeme = construire_prompt_rag(question, top_docs)
    
    messages = [
        {"role": "system", "content": prompt_systeme},
        {"role": "user", "content": question}
    ]
    
    reponse = _client.chat_completion(
        model=MODELE_LLM,
        messages=messages, 
        max_tokens=150
    )
    return reponse.choices[0].message.content


if __name__ == "__main__":
    q = "Je veux réserver la salle municipale, comment faire ?"
    print("Réponse IA :", interroger_rag(q))
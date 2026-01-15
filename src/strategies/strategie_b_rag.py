import sys
import os
import torch
from sentence_transformers import SentenceTransformer, util
import json 

# Permet d'importer les modules src.* même si on lance le script depuis un sous-dossier
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.outils.client_ia import obtenir_client_hf, MODELE_LLM

# 1. Chargement du modèle d'embeddings (le "traducteur" texte -> nombres)
print("Chargement du modèle sémantique...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Chargement de la vraie FAQ depuis le fichier JSON
chemin_faq = os.path.join(os.path.dirname(__file__), "../../data/raw/faq_base.json")
with open(chemin_faq, 'r', encoding='utf-8') as f:
    data = json.load(f)

# On extrait les réponses (c'est ce qu'on va chercher sémantiquement)
documents_faq = [
    f"Question: {item['question']} Réponse: {item['answer']}" 
    for item in data['faq']
]
print(f"📚 {len(documents_faq)} documents chargés depuis la FAQ")

# 3. On transforme les phrases en nombres (Vecteurs) une bonne fois pour toutes
corpus_embeddings = embedder.encode(documents_faq, convert_to_tensor=True)

client = obtenir_client_hf()

def interroger_rag(question):
    print(f"\nRecherche pour : {question}")
    
    # A. Recherche du document le plus pertinent
    query_embedding = embedder.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=1)
    
    # On récupère le meilleur résultat
    meilleur_hit = hits[0][0]  # Premier résultat de la première requête
    doc_trouve = documents_faq[meilleur_hit['corpus_id']]
    score = meilleur_hit['score']
    
    print(f"Document trouvé (Pertinence: {score:.4f}) : {doc_trouve}")
    
    # B. Construction de la réponse avec l'IA
    prompt_systeme = f"""
Tu es un assistant de mairie. Utilise EXCLUSIVEMENT le contexte ci-dessous pour répondre.
Si la réponse n'est pas dans le contexte, dis "Je ne sais pas".

CONTEXTE : "{doc_trouve}"
"""
    
    messages = [
        {"role": "system", "content": prompt_systeme},
        {"role": "user", "content": question}
    ]
    
    reponse = client.chat_completion(
        model=MODELE_LLM,
        messages=messages, 
        max_tokens=150
    )
    return reponse.choices[0].message.content

if __name__ == "__main__":
    q = "Je veux réserver la salle municipale, comment faire ?"
    print("Réponse IA :", interroger_rag(q))
import sys
import os
import json
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# Permet d'importer les modules src.* même si on lance le script depuis un sous-dossier
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Variables globales pour le chargement paresseux
_embedder = None
_corpus_embeddings = None
_extracteur = None
_reponses_faq = None

def _charger_ressources():
    global _embedder, _corpus_embeddings, _extracteur, _reponses_faq
    if _extracteur is not None:
        return

    print("🚀 Chargement des ressources pour la Stratégie C...")
    
    # 1. Chargement de la FAQ
    chemin_faq = os.path.join(os.path.dirname(__file__), "../../data/raw/faq_base.json")
    with open(chemin_faq, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    _reponses_faq = [item['answer'] for item in data['faq']]
    documents_recherche = [
        f"Question: {item['question']} Réponse: {item['answer']}" 
        for item in data['faq']
    ]

    # 2. Modèles sémantiques
    _embedder = SentenceTransformer('all-MiniLM-L6-v2')
    _corpus_embeddings = _embedder.encode(documents_recherche, convert_to_tensor=True)

    # 3. Modèle extractif
    model_name = "etalab-ia/camembert-base-squadFR-fquad-piaf"
    from transformers import AutoTokenizer, AutoModelForQuestionAnswering
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)
    
    _extracteur = pipeline(
        "question-answering",
        model=model,
        tokenizer=tokenizer,
        device=-1
    )
    print("✅ Ressources Stratégie C prêtes")



def interroger_extractif(question):
    """
    Stratégie C : Q&A Extractif
    1. Recherche sémantique du document pertinent
    2. Extraction de la réponse exacte avec Roberta
    """
    _charger_ressources()
    print(f"\n--- Stratégie C : Q&A Extractif ---")
    print(f"Question : {question}")
    
    # A. Recherche du document le plus pertinent
    query_embedding = _embedder.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, _corpus_embeddings, top_k=1)
    
    meilleur_hit = hits[0][0]
    index_doc = meilleur_hit['corpus_id']
    score = meilleur_hit['score']
    
    # On utilise la RÉPONSE complète comme contexte
    contexte = _reponses_faq[index_doc]
    
    print(f"Document trouvé (Pertinence: {score:.4f})")
    print(f"Contexte : {contexte[:100]}...")
    
    # B. Extraction de la réponse exacte
    try:
        resultat = _extracteur(question=question, context=contexte)
        
        reponse_extraite = resultat['answer']
        confiance = resultat['score']
        
        print(f"\n✅ Réponse extraite (Confiance: {confiance:.2%}) :")
        print(f"   {reponse_extraite}")
        
        # Validation du score de confiance
        return valider_reponse(reponse_extraite, confiance)
        
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction : {e}")
        return "Je n'ai pas pu extraire une réponse précise du document."


def valider_reponse(reponse: str, score: float, seuil: float = 0.20) -> str:
    """
    Vérifie si la réponse extraite est assez fiable.
    Si le score est trop bas, on préfère dire qu'on ne sait pas.
    """
    if score < seuil:
        return f"Je ne suis pas assez sûr de la réponse (Confiance: {score:.1%}). Pouvez-vous reformuler ?"
    return reponse


if __name__ == "__main__":
    # Test avec une question
    q = "Comment immatriculer une voiture ?"
    reponse = interroger_extractif(q)
    
    print("\n" + "="*60)
    print("RÉPONSE FINALE :")
    print(reponse)  
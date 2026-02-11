# ============================================================
# IMPORTS
# ============================================================

# FastAPI : le framework pour créer l'API
from fastapi import FastAPI, HTTPException

# Pydantic : pour valider les données entrantes/sortantes
from pydantic import BaseModel

# Pour mesurer le temps de réponse
import time

# Pour pouvoir importer nos stratégies
import sys
import os

# Ajoute le dossier parent au path Python
# Cela permet d'importer src.strategies.*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Import des 3 stratégies qu'on a déjà créées
from src.strategies.strategie_a_llm_seul import executer_strategie_a
from src.strategies.strategie_b_rag import interroger_rag
from src.strategies.strategie_c_extractif import interroger_extractif

# ============================================================
# CRÉATION DE L'APPLICATION
# ============================================================

# Crée l'application FastAPI avec des métadonnées
app = FastAPI(
    title="API FAQ Collectivité Territoriale",
    description="Assistant intelligent pour répondre aux questions des citoyens",
    version="1.0.0"
)

# ============================================================
# MODÈLES DE DONNÉES (Pydantic)
# ============================================================

# Ce que l'utilisateur envoie à l'API
class QuestionRequest(BaseModel):
    question: str                    # La question posée
    strategie: str = "C"            # La stratégie à utiliser (A, B ou C), défaut: B

# Ce que l'API renvoie
class ReponseResponse(BaseModel):
    question: str                    # La question posée
    strategie: str                   # La stratégie utilisée
    reponse: str                     # La réponse générée
    temps_ms: int                    # Temps de traitement en millisecondes

# ============================================================
# ENDPOINTS (Routes de l'API)
# ============================================================

# Route de base : vérifier que l'API fonctionne
@app.get("/")
def accueil():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API FAQ Collectivité Territoriale",
        "documentation": "/docs",
        "strategies_disponibles": ["A", "B", "C"]
    }

# Route principale : poser une question
@app.post("/question", response_model=ReponseResponse)
def poser_question(requete: QuestionRequest):
    """
    Pose une question à l'assistant FAQ.
    
    - **question** : La question à poser
    - **strategie** : A (LLM seul), B (RAG), ou C (Extractif)
    """
    
    # Vérifier que la stratégie est valide
    if requete.strategie not in ["A", "B", "C"]:
        raise HTTPException(
            status_code=400, 
            detail="Stratégie invalide. Utilisez A, B ou C."
        )
    
    # Mesurer le temps de début
    debut = time.time()
    
    # Appeler la bonne stratégie selon le choix
    try:
        if requete.strategie == "A":
            reponse = executer_strategie_a(requete.question)
        elif requete.strategie == "B":
            reponse = interroger_rag(requete.question)
        else:  # C
            reponse = interroger_extractif(requete.question)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors du traitement : {str(e)}"
        )
    
    # Calculer le temps écoulé
    temps_ms = int((time.time() - debut) * 1000)
    
    # Retourner la réponse
    return ReponseResponse(
        question=requete.question,
        strategie=requete.strategie,
        reponse=reponse,
        temps_ms=temps_ms
    )

# Route pour lister les stratégies disponibles
@app.get("/strategies")
def lister_strategies():
    """Liste les stratégies disponibles avec leurs descriptions"""
    return {
        "strategies": [
            {
                "id": "A",
                "nom": "LLM Seul",
                "description": "Utilise uniquement le modèle de langage"
            },
            {
                "id": "B", 
                "nom": "RAG",
                "description": "Recherche sémantique + génération"
            },
            {
                "id": "C",
                "nom": "Extractif",
                "description": "Extraction de réponse exacte"
            }
        ]
    }
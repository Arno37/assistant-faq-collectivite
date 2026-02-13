import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Chargement unique des variables d'environnement
load_dotenv()
token = os.getenv("HF_TOKEN")

MODELE_LLM = "mistralai/Mistral-7B-Instruct-v0.2"

# Configuration centralisée du client
def obtenir_client_hf():
    """Crée et retourne un client HuggingFace configuré avec le token."""
    if not token:
        raise ValueError("Le token HF_TOKEN n'a pas été trouvé dans le fichier .env")
    return InferenceClient(token=token)

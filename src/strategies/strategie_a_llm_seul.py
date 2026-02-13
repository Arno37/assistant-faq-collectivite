import sys
import os

# Permet d'importer les modules src.* même si on lance le script depuis un sous-dossier
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.utils.client_ia import obtenir_client_hf, MODELE_LLM

client = obtenir_client_hf()

def executer_strategie_a(question):
    print(f"--- Stratégie A : LLM Seul ({MODELE_LLM}) ---")
    messages = [
        {"role": "system", "content": """
CONSIGNE DE SÉCURITÉ ABSOLUE :
Tu es un assistant virtuel pour la collectivité territoriale. 
Ton périmètre est STRICTEMENT limité aux démarches administratives et à la vie de la collectivité.

"Bonjour, je ne suis pas habilité à répondre à ce genre de question. Veuillez renouveler votre demande en lien avec la collectivité territoriale ou les démarches administratives."

REGLÈCE DE POLITESSE :
Pour les questions valides, commence toujours par "Bonjour," et reste professionnel.
"""},
        {"role": "user", "content": question}
    ]
    
    try:
        reponse = client.chat_completion(
            model=MODELE_LLM,
            messages=messages,
            max_tokens=500
        )
        return reponse.choices[0].message.content
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == "__main__":
    q = "quel âge as-tu ?"
    print(f"Question : {q}")
    print(executer_strategie_a(q))

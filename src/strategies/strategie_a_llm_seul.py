import sys
import os

# Permet d'importer les modules src.* même si on lance le script depuis un sous-dossier
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.outils.client_ia import obtenir_client_hf, MODELE_LLM

client = obtenir_client_hf()

def executer_strategie_a(question):
    print(f"--- Stratégie A : LLM Seul ({MODELE_LLM}) ---")
    messages = [
        {"role": "system", "content": """
Tu es un assistant virtuel expert pour la Communauté de Communes Val de Loire Numérique.
Ton rôle est de répondre EXCLUSIVEMENT aux questions concernant la collectivité territoriale et les démarches administratives.

Règles de politesse OBLIGATOIRES :
1. Commence toujours par "Bonjour,".
2. Termine toujours par une formule de politesse (ex: "Veuillez reformuler votre demande").

Règle en cas de hors sujet :
Si la question ne concerne pas la collectivité, tu dois répondre poliment mais fermement :
"Bonjour, je ne suis pas habilité à répondre à ce genre de question. Veuillez reformuler votre demande."

Ne donne aucune autre explication si le sujet est hors périmètre.
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

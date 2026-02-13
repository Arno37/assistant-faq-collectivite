import requests 
import json

def test_systeme_reponse_mairie():
    """ Test du système complet : de l'API jusqu'à l'IA """
    
    # 1. Configuration
    url = "http://127.0.0.1:8000/question"
    donnees = {
        "question": "Comment obtenir un acte de naissance ?", 
        "strategie": "B"
    }
    
    print(f"\n🚀 Lancement du TEST SYSTÈME")
    print(f"📡 Appel de l'URL : {url}")
    print(f"❓ Question envoyée : {donnees['question']}")

    # 2. Exécution de la requête
    try:
        reponse = requests.post(url, json=donnees)
        resultat = reponse.json()
        
        print(f"✅ Status Code : {reponse.status_code}")
        print(f"📝 Réponse reçue de l'API :\n{resultat['reponse']}\n")
        print(f"⏱️ Temps de réponse : {resultat.get('temps_ms', 'N/A')}ms")

        # 3. Vérifications (Assertions)
        assert reponse.status_code == 200
        assert "Bonjour" in resultat["reponse"]
        # On vérifie qu'un mot clé lié à la réponse soit présent
        assert "ligne" in resultat["reponse"] or "internet" in resultat["reponse"] or "mairie" in resultat["reponse"]
        
        print("\n🏆 TEST SYSTÈME RÉUSSI : La chaîne complète fonctionne !")

    except requests.exceptions.ConnectionError:
        print("\n❌ ERREUR : Le serveur API n'est pas lancé !")
        print("Pensez à faire : python3 -m uvicorn src.api.main:app --reload")

if __name__ == "__main__":
    # On peut lancer ce test directement avec python3 tests/systeme/test_app.py
    test_systeme_reponse_mairie()
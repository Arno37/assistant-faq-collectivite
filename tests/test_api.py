# ============================================================
# IMPORTS
# ============================================================
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Import de l'application FastAPI
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.api.main import app

# ============================================================
# CONFIGURATION
# ============================================================

# Crée un client de test (simule des requêtes HTTP)
client = TestClient(app)

# ============================================================
# TESTS DE LA ROUTE GET /
# ============================================================

def test_accueil():
    """Test que la page d'accueil fonctionne"""
    print("\n🔍 [TEST] Appel de la racine / ...")
    response = client.get("/")
    
    print(f"   👉 Status Code reçu : {response.status_code}")
    assert response.status_code == 200
    
    data = response.json()
    print(f"   👉 Données reçues : {data}")
    assert "message" in data
    assert "documentation" in data
    assert "strategies_disponibles" in data
    print("   ✅ Vérification des champs OK")

# ============================================================
# TESTS DE LA ROUTE GET /strategies
# ============================================================

def test_lister_strategies():
    """Test que la liste des stratégies fonctionne"""
    print("\n🔍 [TEST] Appel de /strategies ...")
    response = client.get("/strategies")
    
    print(f"   👉 Status Code reçu : {response.status_code}")
    assert response.status_code == 200
    
    data = response.json()
    nb_strategies = len(data["strategies"])
    print(f"   👉 Nombre de stratégies trouvées : {nb_strategies}")
    
    assert "strategies" in data
    assert nb_strategies == 3  # A, B, C
    
    # Vérifier que chaque stratégie a un id
    for strategie in data["strategies"]:
        assert "id" in strategie
        assert "nom" in strategie
    print("   ✅ Structure des stratégies OK")

# ============================================================
# TESTS DE LA ROUTE POST /question
# ============================================================

def test_poser_question_strategie_valide():
    """Test qu'on peut poser une question avec une stratégie valide"""
    print("\n🔍 [TEST] Envoi d'une question (Stratégie A)...")
    payload = {"question": "Bonjour", "strategie": "A"}
    response = client.post("/question", json=payload)
    
    print(f"   👉 Status Code reçu : {response.status_code}")
    assert response.status_code == 200
    
    data = response.json()
    print(f"   👉 Réponse partielle : {str(data)[:100]}...")
    assert "question" in data
    assert "strategie" in data
    assert "reponse" in data
    assert "temps_ms" in data
    assert data["strategie"] == "A"
    print("   ✅ Champs de réponse validés")


def test_poser_question_strategie_invalide():
    """Test qu'une stratégie invalide retourne une erreur"""
    
    response = client.post(
        "/question",
        json={"question": "Bonjour", "strategie": "Z"}  # Z n'existe pas !
    )
    
    # Doit retourner une erreur 400 (Bad Request)
    assert response.status_code == 400


def test_poser_question_sans_question():
    """Test qu'une requête sans question retourne une erreur"""
    
    response = client.post(
        "/question",
        json={"strategie": "B"}  # Pas de "question" !
    )
    
    # Doit retourner une erreur 422 (Validation Error)
    assert response.status_code == 422


def test_erreur_500_api():
    """Simule un crash interne pour vérifier le retour 500"""
    print("\n🧨 [TEST] Simulation d'un crash serveur (Erreur 500)...")
    
    # On "Sabote" la stratégie A pour qu'elle plante
    with patch("src.strategies.strategie_a_llm_seul.executer_strategie_a") as mock_crash:
        mock_crash.side_effect = Exception("Boom ! Explosion simulée")
        
        # On appelle l'API normalement
        response = client.post("/question", json={"question": "Test", "strategie": "A"})
        
        print(f"   👉 Status Code reçu : {response.status_code}")
        assert response.status_code == 500
        assert "Boom" in response.json()["detail"]
        print("   ✅ L'API a bien géré le crash !")



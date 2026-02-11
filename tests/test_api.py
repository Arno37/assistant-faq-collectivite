# ============================================================
# IMPORTS
# ============================================================
import pytest
from fastapi.testclient import TestClient

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
    
    # 1. Faire une requête GET sur /
    response = client.get("/")
    
    # 2. Vérifier que le statut est 200 (OK)
    assert response.status_code == 200
    
    # 3. Vérifier que la réponse contient les bonnes clés
    data = response.json()
    assert "message" in data
    assert "documentation" in data
    assert "strategies_disponibles" in data

# ============================================================
# TESTS DE LA ROUTE GET /strategies
# ============================================================

def test_lister_strategies():
    """Test que la liste des stratégies fonctionne"""
    
    response = client.get("/strategies")
    
    assert response.status_code == 200
    
    data = response.json()
    assert "strategies" in data
    assert len(data["strategies"]) == 3  # A, B, C
    
    # Vérifier que chaque stratégie a un id
    for strategie in data["strategies"]:
        assert "id" in strategie
        assert "nom" in strategie

# ============================================================
# TESTS DE LA ROUTE POST /question
# ============================================================

def test_poser_question_strategie_valide():
    """Test qu'on peut poser une question avec une stratégie valide"""
    
    response = client.post(
        "/question",
        json={"question": "Bonjour", "strategie": "A"}
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert "question" in data
    assert "strategie" in data
    assert "reponse" in data
    assert "temps_ms" in data
    assert data["strategie"] == "A"


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



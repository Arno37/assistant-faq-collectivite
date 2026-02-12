import pytest
from src.strategies.strategie_b_rag import interroger_rag

def test_integration_rag_avec_vraie_faq():
    """
    Vérifie que la stratégie RAG arrive à extraire une info
    pertinente de ta vraie base FAQ (faq_base.json).
    """
    # ARRANGE
    question = "Quels sont les horaires de la déchetterie ?"
    
    # ACT
    reponse = interroger_rag(question)
    
    # ASSERT
    assert isinstance(reponse, str)
    # On vérifie que la réponse contient des éléments clés de ta FAQ
    # pour prouver que l'intégration avec le fichier JSON fonctionne.
    assert "9h" in reponse or "18h" in reponse
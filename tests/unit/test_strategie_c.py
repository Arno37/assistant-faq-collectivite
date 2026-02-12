from src.strategies.strategie_c_extractif import valider_reponse

def test_valider_reponse_confiante():
    """Si le score est haut, on garde la réponse."""
    reponse = "C'est 14h00."
    score = 0.95
    resultat = valider_reponse(reponse, score)
    assert resultat == "C'est 14h00."

def test_valider_reponse_douteuse():
    """Si le score est bas, on rejette la réponse."""
    reponse = "Peut-être..."
    score = 0.05
    resultat = valider_reponse(reponse, score)
    assert "Je ne suis pas assez sûr" in resultat
    assert "5.0%" in resultat  # Vérifie que le pourcentage est affiché

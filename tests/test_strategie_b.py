from src.strategies.strategie_b_rag import construire_prompt_rag

def test_construire_prompt_rag_simple():
    """
    Vérifie que le prompt est bien construit avec un contexte simple.
    """
    # 1. ARRANGE (Préparation des ingrédients)
    ma_question = "C'est quoi le RSA ?"
    mon_contexte = [
        "Le RSA est une aide financière.",
        "Il faut avoir 25 ans pour le RSA."
    ]

    # 2. ACT (Action : On appelle la fonction)
    resultat = construire_prompt_rag(ma_question, mon_contexte)

    # 3. ASSERT (Vérification du résultat)
    # On vérifie que le texte contient bien les infos importantes (le contexte)
    # Note: La question n'est PAS dans ce prompt système, elle est envoyée à part à l'IA.
    assert "Le RSA est une aide financière." in resultat
    assert "Il faut avoir 25 ans" in resultat
    assert "Tu es un assistant" in resultat  # Vérifie que l'instruction système est là

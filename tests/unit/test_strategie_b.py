from src.strategies.strategie_b_rag import construire_prompt_rag

def test_construire_prompt_rag():
    """Vérifie que le prompt contient bien le contexte et la question"""
    print("\n🚧 [TEST] Construction du prompt RAG...")
    
    question = "C'est quoi le RSA ?"
    contexte = ["Le RSA est une allocation."]
    
    prompt = construire_prompt_rag(question, contexte)
    
    # Vérifications
    assert "assistant de mairie" in prompt
    assert "CONTEXTE :" in prompt
    assert "Le RSA est une allocation." in prompt

    
    print("   ✅ Le prompt contient tous les éléments requis.")

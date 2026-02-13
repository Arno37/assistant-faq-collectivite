import os

def charger_documents(dossier_data="data"):
    """
    Charge les fichiers texte (.txt, .md) depuis le dossier spécifié.
    Retourne une liste de chaînes de caractères (le contenu des fichiers).
    """
    documents = []
    
    # Vérifie si le dossier existe, sinon le crée pour éviter une erreur
    if not os.path.exists(dossier_data):
        os.makedirs(dossier_data)
        print(f"Dossier '{dossier_data}' créé.")
        return []

    # Parcourt tous les fichiers du dossier
    for fichier in os.listdir(dossier_data):
        chemin_complet = os.path.join(dossier_data, fichier)
        
        # On ne traite que les fichiers texte simples pour l'instant
        if fichier.endswith(".txt") or fichier.endswith(".md"):
            try:
                with open(chemin_complet, "r", encoding="utf-8") as f:
                    contenu = f.read()
                    # On ajoute le nom du fichier au début pour le contexte
                    documents.append(f"Source: {fichier}\nContent: {contenu}")
            except Exception as e:
                print(f"Erreur lors de la lecture de {fichier}: {e}")
                
    return documents

import unicodedata
import re

def nettoyer_texte(texte):
    """
    Nettoie le texte : minuscule, suppression des accents et des caractères spéciaux simples.
    """
    if not texte:
        return ""
    
    # Passage en minuscules
    texte = texte.lower()
    
    # Suppression des accents
    texte = ''.join(
        c for c in unicodedata.normalize('NFD', texte)
        if unicodedata.category(c) != 'Mn'
    )
    
    # Suppression de la ponctuation inutile (garde lettres et chiffres)
    texte = re.sub(r'[^a-zA-Z0-9\s]', ' ', texte)
    
    # Suppression des espaces en trop
    texte = ' '.join(texte.split())
    
    return texte

import os
import subprocess

# Liste des fichiers HTML à convertir
html_files = [
    "docs/benchmark/GRILLE_EVALUATION.html",
    "docs/day_1/note_de_cadrage.html",
    "docs/day_1/rapport_veille_technique.html",
    "docs/day_2/grille_evaluation.html",
    "docs/day_2/protocole_benchmark.html",
    "rapports/PRESENTATION.html",
    "rapports/RAPPORT.html",
    "rapports/BENCHMARK.html"
]

# Chemin vers Chrome sur Mac (standard)
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def convert_to_pdf(html_path):
    if not os.path.exists(html_path):
        print(f"⚠️ Fichier non trouvé : {html_path}")
        return

    pdf_path = html_path.replace(".html", ".pdf")
    
    # Commande Chrome Headless pour imprimer en PDF
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    
    print(f"📄 Conversion de {html_path} en PDF...")
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Succès : {pdf_path}")
    except Exception as e:
        print(f"❌ Erreur pour {html_path} : {str(e)}")

if __name__ == "__main__":
    for file in html_files:
        convert_to_pdf(file)
    print("\n🎉 Toutes les conversions sont terminées !")

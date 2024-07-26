import fitz  # PyMuPDF
import threading
from collections import Counter
import re

# Fonction pour extraire le texte du PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Fonction pour analyser les données et calculer les statistiques
def analyze_schedule(text, result, lock):
    en_ligne_count = len(re.findall(r'\ben ligne\b', text, re.IGNORECASE))
    salle_count = len(re.findall(r'\bsalle\b', text, re.IGNORECASE))
    
    with lock:
        result["en_ligne"] += en_ligne_count
        result["salle"] += salle_count

def main():
    pdf_path = "emplois_du_temps.pdf"
    
    # Extraire le texte du PDF
    text = extract_text_from_pdf(pdf_path)
    
    # Afficher une partie du texte extrait pour vérification
    print("Extrait du texte extrait du PDF (premiers 1000 caractères) :")
    print(text[:1000])
    
    # Initialiser les compteurs et le verrou
    result = Counter()
    lock = threading.Lock()
    
    # Créer des threads pour analyser le texte
    threads = []
    num_threads = 4
    for i in range(num_threads):
        thread = threading.Thread(target=analyze_schedule, args=(text, result, lock))
        threads.append(thread)
        thread.start()
    
    # Attendre que tous les threads se terminent
    for thread in threads:
        thread.join()
    
    # Calculer le nombre total de séances
    total_seances = result["en_ligne"] + result["salle"]
    
    # Calculer les pourcentages
    if total_seances > 0:
        en_ligne_percentage = (result["en_ligne"] / total_seances) * 100
        salle_percentage = (result["salle"] / total_seances) * 100
    else:
        en_ligne_percentage = 0
        salle_percentage = 0
    
    # Afficher les résultats
    print("Nombre de séances en ligne :", result["en_ligne"])
    print("Nombre de séances salle :", result["salle"])
    print("Pourcentage de séances en ligne :", en_ligne_percentage, "%")
    print("Pourcentage de séances salle :", salle_percentage, "%")

if __name__ == "__main__":
    main()

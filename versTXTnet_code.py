import os
import time
import re

from bs4 import BeautifulSoup
from pdf2image import convert_from_path
import ebooklib
from ebooklib import epub
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from nltk.corpus import stopwords


def get_file_path():
    """Fonction interactive qui demande le chemin du fichier à importer

    Returns:
        str: nom du chemin vers le fichier
    """
    while True:
        file_path = input("Entre le chemin vers le fichier PDF (.pdf), ePub (.epub) ou text (.txt) : ")
        if file_path.endswith('.pdf') or file_path.endswith('.epub') or file_path.endswith('.txt'):
            if os.path.exists(file_path):
                return file_path
            else:
                print("Le fichier n'existe pas. Entre le bon chemin.")
        else:
            print("Le format indiqué n'est pas adéquat. Fournis un fichier de type .pdf, .epub ou .txt")



def load_txt(file_path):
    """Fonctions de chargement d'un fichier .txt

    Args:
        file_path (str): chemin du fichier

    Returns:
        str: chaine de caractères (texte complet du fichier)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ').replace('\xad', '').replace('|', ' ').replace(' – ', ' ').strip()
    return text


def load_pdf(file_path):
    """Océrisation avec PyPDF2

    Args:
        file_path (str): chemin du fichier

    Returns:
        str: chaine de caractères (texte complet du fichier)
    """
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''.join([page.extract_text() for page in reader.pages])
        text = text.replace('-\n', '').replace('\n', ' ').replace('\xad', '').replace('|', ' ').replace(' – ', ' ').strip()
    return text


def extract_text_with_tesseract(file_path, lang='fra'):
    """Océrisation avec tesseract (plus lent qu'avec PyPDF2)

    Args:
        file_path (str): chemin du fichier
        lang (str, optional): Langue du moteur de reconnaissance de caractères. Par défaut 'fra'.

    Raises:
        ValueError: Erreur si fichier le fichier n'est pas traitable par tesseract

    Returns:
        str: chaine de caractères (texte complet du fichier)
    """
    
    
    file_extension = file_path.split('.')[-1].lower()
    if file_extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
        # Extraction des caractères à partir de fichiers images
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang=lang)
        
    elif file_extension == 'pdf':
        # Conversion des pages du texte en images
        images = convert_from_path(file_path)
        
        # Extraction des chaines
        texts = []
        for image in images:
            page_text = pytesseract.image_to_string(image, lang=lang)
            texts.append(page_text)
        
        # Assemblage des chaines
        text = '\n'.join(texts)

    else:
        raise ValueError(f"Unsupported file type '{file_extension}'. Supported types are JPG, PNG, BMP, TIFF, and PDF.")
    
    text = re.sub(r'-\s+', '', text)

    return text


def load_epub(file_path):
    """Extraction du texte de fichiers epub

    Args:
        file_path (str): chemin du fichier

    Returns:
        str: chaine de caractères (texte complet)
    """
    book = epub.read_epub(file_path)
    text = ''
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        lines = item.get_content().decode('utf-8').splitlines()
        html_text = ' '.join(lines)
        soup = BeautifulSoup(html_text, 'html.parser')
        text += soup.get_text(separator=' ')
    text = text.replace('-\n', ' ').replace('\n', ' ').replace('\xad', '').replace('|', ' ').replace(' – ', ' ').strip()
    return text


def truncate_text_start(text):
    """Fonctions de troncature (début et fin)

    Args:
        text (str): texte 

    Returns:
        str: texte tronqué (optionnel)
    """
    while True:
        num_words_to_print = min(1000, len(text.split()) // 2)
        print("DÉBUT DU TEXTE: " + ' '.join(text.split()[:num_words_to_print]))
        truncate_text = input("Veux-tu retrancher une partie du texte? (oui/non): ")
        if truncate_text.lower() == 'oui':
            sequence = input("Indique la dernière séquence de caractères à CONSERVER: ")
            if sequence in text:
                text = text[text.index(sequence):]
                print(f"Le texte a été coupé. La séquence '{sequence}' forme maintenant le début du texte.")
            else:
                print("La séquence de caractères n'a pas été trouvée. Ressaye.")
        elif truncate_text.lower() == 'non' or truncate_text.strip() == '':
            break
        else:
            print("Entrée non valide. Entre 'oui' or 'non'.")
    return text


def truncate_text_end(text):
    while True:
        num_words_to_print = min(1000, len(text.split()) // 2)
        print("FIN DU TEXTE: " + ' '.join(text.split()[-num_words_to_print:]))
        truncate_text = input("Veux-tu couper la fin du texte? (oui/non): ")
        if truncate_text.lower() == 'oui':
            sequence = input("Entre le début de la séquence qui doit être coupée jusqu'à la fin: ")
            if sequence in text:
                text = text[:text.index(sequence)]
                print(f"Le texte a été coupé. La séquence '{sequence}' et tout ce qui vient après a été coupé.")
            else:
                print("La séquence n'a pas été trouvée dans le texte. Essaye à nouveau.")
        elif truncate_text.lower() == 'non' or truncate_text.strip() == '':
            break
        else:
            print("Entrée non valide. Entre 'oui' or 'non'.")
    return text



    """Fonction de prétraitement:

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
french_stopwords = set(stopwords.words('french'))
english_stopwords = set(stopwords.words('english'))

# I'll reformat and reindent the provided function code.

def process_text(text):
    """
    Traitement interactif du texte:
    1. Removing punctuation.
    2. Removing numbers.
    3. Removing symbols.
    4. Removing stopwords.
    5. Transforming case.
    6. Converting non-ASCII characters to ASCII.

    Returns:
        str: texte traité (optionnel)
    """
    
    # 1. Ask user if they want to remove punctuation
    choice = input("Veux-tu supprimer la ponctuation du texte? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = re.sub(r'[.,!?]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
   
    # 2. Ask user if they want to remove numbers
    choice = input("Veux-tu supprimer les nombres du texte? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = re.sub(r'\b\d+\b', ' ', text)
        text = re.sub(r'\s+', ' ', text)

    # 3. Ask user if they want to remove symbols (excluding punctuation)
    choice = input("Veux-tu supprimer les symboles (hors ponctuation) du texte? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = re.sub(r'[^\w\s.,!?]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
    
    # 4. Ask user if they want to use lowercase
    choice = input("Veux-tu transformer la casse (minuscules)? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = text.lower()
    
    # 5. Ask if the user wants to remove stopwords
    remove_stopwords = input("Veux-tu supprimer les mots vides (stopwords) ? (oui/non): ").strip().lower()
    
    if remove_stopwords == "oui":
        # Ask for the language of the stopwords
        language_choice = input("Quelle langue pour la liste des mots vides ? (fr/an): ").strip().lower()
        
        if language_choice == "fr":
            current_stopwords = french_stopwords
        elif language_choice == "an":
            current_stopwords = english_stopwords
        else:
            print("Choix de langue non valide. Utilisation des stopwords français par défaut.")
            current_stopwords = french_stopwords
        
        # Display the chosen stopwords list
        print("\nListe actuelle des mots vides:")
        print(", ".join(sorted(current_stopwords)))
        
        # Ask if user wants to remove any stopwords from this list iteratively
        while True:
            remove_word = input("Veux-tu enlever des mots de cette liste ? (oui/non): ").strip().lower()
            
            if remove_word == "oui":
                words_to_remove = input("Entre les mots à enlever, séparés par des virgules: ").strip().lower().split(',')
                for word in words_to_remove:
                    current_stopwords.discard(word.strip())
                print("\nListe mise à jour des mots vides:")
                print(", ".join(sorted(current_stopwords)))
            elif remove_word == "non":
                break
        
        # Ask if user wants to add new stopwords to the list iteratively
        while True:
            add_word = input("Veux-tu ajouter des mots à cette liste ? (oui/non): ").strip().lower()
            
            if add_word == "oui":
                words_to_add = input("Entre les mots à ajouter, séparés par des virgules: ").strip().lower().split(',')
                for word in words_to_add:
                    current_stopwords.add(word.strip())
                print("\nListe mise à jour des mots vides:")
                print(", ".join(sorted(current_stopwords)))
            elif add_word == "non":
                break
        
        # Apply the final stopwords removal
        words = text.split()
        text = ' '.join([word for word in words if word.lower() not in current_stopwords])

    # 6. Ask user if they want to convert text to ASCII
    choice = input("Veux-tu convertir le texte en ASCII (ceci supprimera les caractères spéciaux)? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = text.encode("ascii", errors="ignore").decode()

    return text

# The function has been reformatted and reindented.


def load_file(file_path):
    """Fonction qui utilise l'une des fonctions de lecture, selon le type de fichier identifié

    Args:
        file_path (str): chemin du fichier

    Raises:
        ValueError: erreur si le fichier n'est pas de type pdf, epub ou txt (exlusion des formats image pour l'instant)

    Returns:
        str: texte
    """
    start_time = time.time()
    file_type = file_path.split('.')[-1]
    if file_type not in ['pdf', 'epub', '.txt']:
        raise ValueError(f"Unsupported file type '{file_type}'")
    
    if file_type == 'txt':
        text = load_txt(file_path)
    elif file_type == 'pdf':
        # text = load_pdf(file_path)
        text = extract_text_with_tesseract(file_path)
    elif file_type == 'epub':
        text = load_epub(file_path)
        
    end_time = time.time()  # End time after loading
    
    duration = end_time - start_time
    print(f"Le fichier a été chargé en {duration:.2f} secondes.")

    return file_type, text

# Fonction pour sauvegarder le résultat:
def save_results(text, file_path):
    """Fonction de sauvegarde du texte lu et traité

    Args:
        text (str): chaine de caractères (texte complet)
        file_path (str): chemin du fichier pour la sauvegarde
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


# Fonction pour la correction interactive du texte océrisé
def correct_ocr_errors_interactive(text):
    """Fonction de correction de mots

    Args:
        text (str): texte

    Returns:
        str: texte
    """
    continue_outer_loop = True
    
    while continue_outer_loop:
        # Apply initial corrections to the entire text
        text = re.sub(r"(\w) ’(\w)", r"\1’\2", text)
        text = re.sub(r' \.', '.', text)
        text = re.sub(r' ,', ',', text)

        # Extract the first 3000 words for inspection and apply the same initial corrections
        words = text.split()
        sample = ' '.join(words[:3000])
        sample = re.sub(r"(\w) ’(\w)", r"\1’\2", sample)
        sample = re.sub(r' \.', '.', sample)
        sample = re.sub(r' ,', ',', sample)
        
        print("\nFirst 3000 words for inspection:")
        print(sample)

        # Obtenir les patterns à corriger post-océrisation
        common_splits = {}
        while True:
            print("\nVeux-tu corriger une chaîne de caractères problématique ? (oui/non)")
            choice = input().strip().lower()

            if choice == 'oui':
                split_word = input("Entre le mot à corriger (ex.: 'tou jours'): ")
                correct_word = input(f"Comment le mot doit-il être écrit '{split_word}' (ex.: 'toujours'): ")
                common_splits[split_word] = correct_word

                # Apply the correction from the dictionary to the entire text and inform the user about the change
                count = text.count(split_word)
                text = text.replace(split_word, correct_word)
                print(f"Le motif '{split_word}' a été trouvé et corrigé {count} fois en '{correct_word}'.")

            elif choice == 'non':
                continue_outer_loop = False
                break
            else:
                print("Choix non valide. Entre 'oui' ou 'non'.")

        # Print the corrected version of the previously shown sample for verification
        corrected_words = text.split()
        corrected_sample = ' '.join(corrected_words[:3000])
        
        print("\nVERSION CORRIGÉE DES PREMIERS 3000 MOTS:")
        print(corrected_sample)

    return text

# Fonction maîtresse
def process_text_pipeline():
    """
    Fonction maîtresse. Assemblage de toutes les fonctions et exécution.

    """
    # Get file path from user
    file_path = get_file_path()

    # Load the text based on the file type
    _, text = load_file(file_path)

    # Offer user to truncate start and end of the text
    text = truncate_text_start(text)
    text = truncate_text_end(text)

    # Correct errors
    correct_ocr_errors_interactive(text)

    # Process the text
    processed_text = process_text(text)

    words = processed_text.split()
    sample = ' '.join(words[:3000])
    print(sample)

    # Save the results
    output_file_path = input("Entre le chemin pour sauvegarder le résultat: ")
    save_results(processed_text, output_file_path)
    print(f"Le texte a été traité et sauvegardé dans {output_file_path}")

process_text_pipeline()
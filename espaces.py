# Installer les modules en exécutant la ligne suivante dans le Terminal:
# pip install -r requirements.txt

import os
import re
import string
import random
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from PyPDF2 import PdfReader

def get_file_path():
    while True:
        file_path = input("Entre le chemin vers le fichier PDF (.pdf), ePub (.epub) ou text (.txt) : ")
        if file_path.endswith('.pdf') or file_path.endswith('.epub') or file_path.endswith('.txt'):
            if os.path.exists(file_path):
                return file_path
            else:
                print("Le fichier n'existe pas. Entre le bon chemin.")
        else:
            print("Le format indiqué n'est pas adéquat. Fournis un fichier de type .pdf, .epub ou .txt")


# Fonctions de chargement des différents types de fichiers
def load_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', ' ').replace('\xad', '').replace('|', ' ').replace(' – ', ' ').strip()
    return text

def load_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''.join([page.extract_text() for page in reader.pages])
    return text.replace('-\n', '').replace('\n', ' ').replace('\xad', '').replace('|', ' ').replace(' – ', ' ').strip()

def load_epub(file_path):
    book = epub.read_epub(file_path)
    text = ''
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        lines = item.get_content().decode('utf-8').splitlines()
        html_text = ' '.join(lines)
        soup = BeautifulSoup(html_text, 'html.parser')
        text += soup.get_text(separator=' ')
    text = text.replace('-\n', ' ').replace('\n', ' ').replace('\xad', '').replace('|', ' ').replace(' – ', ' ').strip()
    return text

def identify_spaces(text):
    # Dictionary of different types of Unicode spaces
    spaces = {
        "Space (U+0020)": "\u0020",
        "Non-breaking space (U+00A0)": "\u00A0",
        "En space (U+2002)": "\u2002",
        "Em space (U+2003)": "\u2003",
        "Three-per-em space (U+2004)": "\u2004",
        "Four-per-em space (U+2005)": "\u2005",
        "Six-per-em space (U+2006)": "\u2006",
        "Figure space (U+2007)": "\u2007",
        "Punctuation space (U+2008)": "\u2008",
        "Thin space (U+2009)": "\u2009",
        "Hair space (U+200A)": "\u200A",
        "Zero width space (U+200B)": "\u200B",
        "Narrow no-break space (U+202F)": "\u202F",
        "Medium mathematical space (U+205F)": "\u205F",
        "Ideographic space (U+3000)": "\u3000"
    }
    
    found_spaces = {name: code for name, code in spaces.items() if code in text}
    
    return found_spaces



# Fonction de prétraitement:
def process_text(text):
    # Ask user if they want to remove numbers
    choice = input("Veux-tu supprimer les nombres du texte? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = re.sub(r'\b\d+\b', ' ', text)
        text = re.sub(r'\s+', ' ', text)

    # Ask user if they want to remove symbols (excluding punctuation)
    choice = input("Veux-tu supprimer les symboles (hors ponctuation) du texte? (oui/non): ").strip().lower()
    if choice == 'oui':
        # This regex will match symbols but not alphanumeric characters or punctuation
        text = re.sub(r'[^\w\s.,!?]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
    
    # Ask user if they want to remove punctuation
    choice = input("Veux-tu supprimer la ponctuation du texte? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = re.sub(r'[.,!?]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

    # Ask user if they want to convert text to ASCII
    choice = input("Veux-tu convertir le texte en ASCII (ceci supprimera les caractères spéciaux)? (oui/non): ").strip().lower()
    if choice == 'oui':
        text = text.encode("ascii", errors="ignore").decode()

    return text


def load_file(file_path):
    file_type = file_path.split('.')[-1]
    if file_type not in ['pdf', 'epub', '.txt']:
        raise ValueError(f"Unsupported file type '{file_type}'")
    
    if file_type == 'txt':
        text = load_txt(file_path)
    elif file_type == 'pdf':
        text = load_pdf(file_path)
    elif file_type == 'epub':
        text = load_epub(file_path)

    return file_type, text


# Fonction maîtresse
def process_text_pipeline():
    # Get file path from user
    file_path = get_file_path()

    # Load the text based on the file type
    _, text = load_file(file_path)

    # Correct errors
    identify_spaces(text)

    spaces_in_text = identify_spaces(text)
    print(spaces_in_text)

process_text_pipeline()
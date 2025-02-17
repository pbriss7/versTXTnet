import streamlit as st
import os
import re
import time
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import ebooklib
from ebooklib import epub
from PIL import Image
import pytesseract
import nltk
from bs4 import BeautifulSoup

# Téléchargement des stopwords si nécessaire
nltk.download("stopwords")
from nltk.corpus import stopwords

# Définition des stopwords
french_stopwords = set(stopwords.words("french"))
english_stopwords = set(stopwords.words("english"))


def load_txt(file_path):
    """Lecture et nettoyage d'un fichier texte."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return clean_text(text)


def load_pdf(file_path):
    """Extraction du texte d'un fichier PDF."""
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    return clean_text(text)


def extract_text_with_tesseract(file_path, lang="fra"):
    """OCR avec Tesseract."""
    images = convert_from_path(file_path)
    text = "\n".join(pytesseract.image_to_string(img, lang=lang) for img in images)
    return clean_text(text)


def load_epub(file_path):
    """Extraction du texte d'un fichier EPUB."""
    book = epub.read_epub(file_path)
    text = ""
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content().decode("utf-8"), "html.parser")
        text += soup.get_text(separator=" ")
    return clean_text(text)


def clean_text(text):
    """Nettoyage initial du texte."""
    text = text.replace("-\n", "").replace("\n", " ").replace("\xad", "").replace("|", " ").strip()
    text = re.sub(r"\s+", " ", text)  # Suppression des espaces multiples
    return text


def truncate_text(text, position, mode="start"):
    """Tronque le texte au début ou à la fin en fonction d'une position donnée."""
    if mode == "start":
        return text[position:]
    elif mode == "end":
        return text[:position]
    return text


def remove_numbers(text):
    """Supprime tous les chiffres du texte, même collés aux mots."""
    return re.sub(r"\d+", "", text)


def process_text(text, remove_punctuation, remove_numbers_flag, lowercase, remove_stopwords_flag, language):
    """Nettoyage avancé du texte en fonction des choix de l'utilisateur."""
    
    if remove_punctuation:
        text = re.sub(r"[.,!?]", " ", text)
    
    if remove_numbers_flag:
        text = remove_numbers(text)

    if lowercase:
        text = text.lower()

    if remove_stopwords_flag:
        stopwords_list = french_stopwords if language == "fr" else english_stopwords
        text = " ".join([word for word in text.split() if word.lower() not in stopwords_list])

    return text


def save_results(text):
    """Prépare le texte à être téléchargé sous forme de fichier."""
    return text.encode("utf-8")  # Convertir en bytes pour le téléchargement


# --------------------------------------------------------------
# Interface Streamlit
# --------------------------------------------------------------

st.title("📝 Convertisseur de texte nettoyé")

uploaded_file = st.file_uploader("Importe un fichier (.txt, .pdf, .epub)", type=["txt", "pdf", "epub"])

if uploaded_file is not None:
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Chargement du fichier
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension == "txt":
        text = load_txt(file_path)
    elif file_extension == "pdf":
        text = load_pdf(file_path)
    elif file_extension == "epub":
        text = load_epub(file_path)
    else:
        st.error("Format non supporté.")
        st.stop()

    st.success("📂 Fichier chargé avec succès !")

    # --- Étape 1: Tronquer le texte au début ---
    st.subheader("📝 Tronquer le début du texte")
    st.text_area("Aperçu du début du texte (5000 premiers caractères)", text[:5000], height=200)
    truncate_start = st.text_input("Indique la séquence de caractères où commencer le texte (laisser vide si inutile)")
    if truncate_start and truncate_start in text:
        text = truncate_text(text, text.index(truncate_start), mode="start")
        st.success("✅ Texte tronqué depuis le début.")

    # --- Étape 2: Tronquer le texte à la fin ---
    st.subheader("📝 Tronquer la fin du texte")
    st.text_area("Aperçu de la fin du texte (5000 derniers caractères)", text[-5000:], height=200)
    truncate_end = st.text_input("Indique la séquence où couper jusqu'à la fin (laisser vide si inutile)")
    if truncate_end and truncate_end in text:
        text = truncate_text(text, text.index(truncate_end), mode="end")
        st.success("✅ Texte tronqué à la fin.")

    # --- Étape 3: Nettoyage et correction OCR ---
    st.subheader("🛠️ Nettoyage du texte")
    remove_punctuation = st.checkbox("Supprimer la ponctuation")
    remove_numbers_flag = st.checkbox("Supprimer tous les chiffres")
    lowercase = st.checkbox("Convertir en minuscules")
    remove_stopwords_flag = st.checkbox("Supprimer les mots vides (stopwords)")
    language = st.radio("Langue des stopwords", ("fr", "en"), index=0)

    if st.button("🔄 Traiter le texte"):
        text_cleaned = process_text(
            text,
            remove_punctuation,
            remove_numbers_flag,
            lowercase,
            remove_stopwords_flag,
            language,
        )
        st.success("✅ Texte nettoyé avec succès !")

        # --- Étape 4: Affichage des 3000 premiers caractères avant sauvegarde ---
        st.subheader("📌 Aperçu du texte final 3000 premiers caractères)")
        st.text_area(
            "Texte final (3000 premiers caractères)", text_cleaned[:5000], height=200
        )

        # --- Étape 5: Sauvegarde ---

        st.subheader("💾 Enregistrement du texte")

        file_name = st.text_input("📁 Nom du fichier de sortie", "texte_nettoye.txt")

        if file_name:
            text_bytes = save_results(text_cleaned)

            # Ajouter un bouton de téléchargement
            st.download_button(
                label="📥 Télécharger le texte nettoyé",
                data=text_bytes,
                file_name=file_name,
                mime="text/plain",
            )
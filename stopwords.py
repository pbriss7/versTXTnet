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

french_stopwords = set(stopwords.words('french'))
english_stopwords = set(stopwords.words('english'))

print(english_stopwords)
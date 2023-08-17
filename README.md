# convertToText

Ce programme permet la lecture, la conversion, le troncature, la correction et le prétraitement d'un texte contenu dans un fichier .epub, .pdf ou .txt. Le texte sauvegardé au terme des opérations est écrit dans un fichier avec une extension .txt.

Le prétraitement inclut des opérations communes telles la suppression des nombres, symboles, signes de ponctuation, l'imposition du bas-de-casse et l'encodage des caractères en ASCII.

L'océrisation par défaut est lente. Elle utilise le package `pytesseract`, qui fournit une océrisation de grande qualité, mais qui suppose la transformation préalable de chaque page du texte en format image. Cette transformation est effectuée grâce au package pdf2image. Par défaut, la fonction de reconnaissance optique `pytesseract.image_to_string` est optimisée pour le français, mais une autre langue peut être proposée dans les réglages de la fonction `extract_text_with_tesseract` du fichier `code`. L'océrisation peut être également faite avec le package PyPDF2. Il s'agit simplement de supprimer le croisillon de la ligne 168 du code et d'en ajouter un à la ligne 169. La fonction qui mobilise le package PyPDF2 sera alors intégrée au pipeline et celle qui recourt à Pytesseract sera mise en suspens.

Avant de lancer le programme, il faut activer l'environnement virtuel avec l'instruction suivante, lancée depuis le terminal dans le dossier où se trouvent les éléments du programme:

`source mien/bin/activate`

On installera également dans cet environnement le logiciel poppler. On peut faire cela en exécutant l'instruction suivante dans le Terminal:

`brew install poppler`

(Le gestionnaire d'installation Homebrew doit être installé sur l'ordinateur.)

En principe, les packages requis sont installés dans l'environnement virtuel activé. S'ils ne le sont pas, exécutez la ligne suivante dans le Terminal:

`pip install -r requirements.txt`

Pour toute question: Pascal Brissette (pascal.brissette@mcgill.ca)


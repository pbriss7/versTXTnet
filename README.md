# versTXT

Ce programme permet la conversion de fichiers .epub et .pdf en fichiers .txt. Il permet également d'exécuter diverses opérations à la volée sur le texte importé avant sa sauvegarde en format texte. Ces opérations sont la suppression de chaines de caractères au début et à la fin du texte, la corrections d'erreurs (mots mal divisés, etc.), la suppression des nombres, symboles, signes de ponctuation, ou encore l'imposition du bas-de-casse ou l'encodage des caractères en ASCII. Des mots vides (stopwords) peuvent également être retirés du texte traité. Les listes proposées sont celles, en français et en anglais, du module nltk, mais l'utilisateur peut enlever ou ajouter des mots à ces listes. Le texte issu de ces opérations est sauvegardé dans un fichier déposé dans le même dossier que le programme.

L'océrisation par défaut est lente. Elle utilise le module pytesseract, qui fournit une océrisation de grande qualité, mais qui suppose la transformation préalable de chaque page du texte en format image. Cette transformation est effectuée grâce au module pdf2image. Dans le script principal, `code.py`, la fonction de reconnaissance optique est optimisée pour le français, mais une autre langue peut être proposée dans les réglages de la fonction `extract_text_with_tesseract`. Une océrisation rapide peut être également faite avec le module PyPDF2. Il s'agit simplement de supprimer, dans le fichier `code.py`, le croisillon de la ligne 168 et d'en ajouter un à la ligne 169. La fonction qui mobilise le module PyPDF2 sera alors intégrée au pipeline et celle qui recourt à Pytesseract sera mise en suspens.

Avant de lancer le programme, il faut installer le logiciel poppler. On peut faire cela en exécutant l'instruction suivante dans le Terminal:

`brew install poppler`

(Le gestionnaire d'installation Homebrew doit être installé sur l'ordinateur. https://brew.sh/)

Pour installer les modules qui ne le sont pas, exécutez la ligne suivante dans le Terminal (ajustez la commande `pip` selon la version Python utilisée. Le programme a été créé avec Python 3.11):

`pip3.11 install -r requirements.txt`

Pour toute question: Pascal Brissette (pascal.brissette@mcgill.ca)


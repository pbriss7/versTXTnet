# versTXTnet

## Description
Ce petit programme permet la conversion de fichiers .epub et .pdf en fichiers .txt. Il permet également d'exécuter diverses opérations à la volée sur le texte avant sa sauvegarde en format texte. Ces opérations sont:

* élimination de chaines de caractères au début et à la fin du texte;
* corrections d'erreurs (mots mal divisés, etc.);
* élimination des nombres, symboles et signes de ponctuation;
* transformation des lettres majuscules en minuscules;
* encodage des caractères en ASCII;
* élimination des mots vides (stopwords). Les listes de mots vides proposées sont celles, en français et en anglais, du module nltk. L'utilisateur est invité à examiner la liste proposée, à en retirer ou à y ajouter des mots.

Le texte issu de ces opérations est sauvegardé dans un fichier qui est déposé dans le même dossier que le programme.

## Océrisation
L'océrisation par défaut est lente (plus ou moins trois minute pour un texte de 150 pages). Elle utilise le module pytesseract, qui fournit une océrisation de grande qualité, mais qui suppose la transformation préalable de chaque page du texte en format image. Cette transformation est effectuée grâce au module pdf2image. Dans le script principal, `code.py`, la fonction de reconnaissance optique est optimisée pour le français, mais une autre langue peut être proposée dans les réglages de la fonction `extract_text_with_tesseract`. Une océrisation rapide peut être également faite avec le module PyPDF2. Il s'agit simplement de supprimer, dans le fichier `code.py`, le croisillon de la ligne suivante:

`# text = load_pdf(file_path)`

et d'ajouter un croisillon à la ligne suivante:

`text = extract_text_with_tesseract(file_path)`.

La fonction qui mobilise le module PyPDF2 sera alors intégrée au pipeline et celle qui recourt à pytesseract sera mise en suspens.

## Installation des modules et lancement du programme
Avant de lancer le programme, il faut installer le logiciel poppler. Sur Mac, on peut faire cela en exécutant l'instruction suivante dans le Terminal:

`brew install poppler`

(Le gestionnaire d'installation Homebrew doit être installé sur l'ordinateur. https://brew.sh/)

Pour installer les modules qui ne le sont pas, exécutez la ligne suivante dans le Terminal (ajustez la commande `pip` selon la version Python utilisée. Le programme a été créé avec Python 3.11):

`pip3.11 install -r requirements.txt`

Pour lancer le programme, on exécute le fichier code.py. Par exemple, dans le Terminal:

`python3.11 code.py`


Pour toute question: Pascal Brissette (pascal.brissette@mcgill.ca)


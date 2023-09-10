## Description
Le programme permet la conversion de fichiers .epub et .pdf en fichiers .txt. Il permet également d'exécuter diverses opérations à la volée sur le texte avant sa sauvegarde en format texte. Ces opérations sont:

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

## Exécution locale du programme
### Le Notebook
La manière la plus simple de lancer le programme est de télécharger le répertoire depuis https://github.com/pbriss7/versTXTnet, d'ouvrir le fichier `versTXTnet_Notebook.ipynb`, puis d'exécuter les cellules les unes à la suite des autres. La dernière ne comprend que la fonction maitresse; en l'exécutant, le programme sera lancé. On demandera à l'usager d'entrer le chemin d'un fichier à traiter. Une fois le travail terminé, le programme demandera à l'usager de fournir un chemin pour enregistrer le texte. Cela peut être aussi simple que "fichier_traite.txt". Le fichier sera alors enregistré dans le répertoire de travail.

Avant de lancer le programme, il faut installer le logiciel poppler. Sur Mac, on peut faire cela en exécutant l'instruction suivante dans le Terminal:

`brew install poppler`

(Le gestionnaire d'installation Homebrew doit être installé sur l'ordinateur. https://brew.sh/)

### Lancement du programme avec Python3.11
Il est recommandé de créer un environnement virtuel avec la version locale ou mise à jour de Python. On importe (ou clone) ensuite le répertoire Github dans cet environnement, puis on ouvre le fichier code.py avec un éditeur Python (ex. VSCode).

Pour installer les modules qui ne le sont pas, exécutez la ligne suivante dans un Terminal de l'environnement (ajustez la commande `pip` selon la version Python utilisée. Le programme a été créé avec Python 3.11):

`pip3.11 install -r requirements.txt`

Pour lancer le programme, on exécute le fichier code.py. Par exemple, dans le Terminal:

`python3.11 versTXTnet_code.py`


Pour toute question: Pascal Brissette (pascal.brissette@mcgill.ca)


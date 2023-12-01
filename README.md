#### Project 2 : Utilisez les bases de Python pour l'analyse de marché.


## Description

Il s'agit d'un programme de scraping Web conçu pour extraire des informations du site Web "Books to scrape". Le but de ce programme est de collecter des données liées aux livres à des fins d'analyse ou à d'autres fins.

+ Rendez-vous dans le dossier contenant le script avec la commande ``cd``

+ Veuillez créer un environnement virtuel.

    d'abord par l'installation virtualenv (si virtualenv n'est pas installé): ``pip install virtualenv`` .

    ou directement  à l'aide de la commande ``python -m venv env.``


+ Activez l'environnement virtuel:
    * Pour le __Shell Bash__ à l'aide de la commande:   ``source env/script/activate``
    * Pour le __terminal windows__ à l'aide de la commande: ``.\env\script\activate.bat``

+ Veuillez installer les packages énumérés dans le fichier __requirement.txt__ à l'aide de la commande:  ``pip install -r requirements.txt``.

+ Lancez le programme avec python en ligne de commande avec l'instruction  " `` python main.py``". main est le script python principal. celui-ci déclenchera l'appel de la fonction «_scrapper_book_to_scrap()_» ,qui amorcera à son tour automatiquement le scrapping du site « Books to scrape ». Le programme commencera à récupérer les données du site Web « Books to scrape ».Le programme va générer des données de 2 types, reparties en 2 dossiers principaux _csv et images_. Les informations textuelles relatives à chaque livre sont regroupées en des catégories corresponds à des fichiers_.csv_ du dossier _csv_ dont les dénominations sont tirées du site web « Books to scrape ». Il en va de même pour les fichiers images, qui sont par contre enregistrés en binaire au format _.jpg_ et regroupés également en catégories qui correspondent à des sous-dossiers du dossier _images_.

+ Si vous rencontrez des problèmes ou avez des suggestions d'amélioration, veuilez m'en informé. 





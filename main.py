# PROJET BOOKS TO SCRAPE (WEB SCRAPPER)
# D'abord créer un environement virtuel  avec: python -m venv env
# Initialiser un repertory local git avec: git init
# Créer le fichier requirements: pip freeze >requirements.txt avec redirection sur le fichier requirements.txt
# Dans .gitignore exclure: les fichiers de l'environement virtuel, les fichiers CSV et images.


# Avec PIP installer les packages néccessaires
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os


def parcourir_toutes_les_categories():
    # Parcours toutes les catégories du site web
    # Cette fonction est appelée par la fonction "scraper_books_to_scrape()"

    url = "http://books.toscrape.com/index.html"  # TO DO: adresse à saisir.
    response = requests.get(url)

    # Réponse de la requête html qui doit etre égale à 200
    if response.status_code == 200:
        html = response.content  # Extraction du contenu de la page html.
        # Création de l'objet soup qui permettra de parser le code html.
        soup = BeautifulSoup(html, "html.parser")
        # Trouve la liste de catégories.
        liste_categories = soup.find(
            "ul", class_="nav nav-list").ul.find_all("li")
        # Initialisation de la liste des urls de différentes catégories.
        liste_urls_categories = []
        for categorie in liste_categories:
            # trouve une partie de l'adresse.
            url_categorie_relative = categorie.a.attrs["href"]
            # création de l'url absolue à partir de l'url relative,par Concaténation du chemin courant et du chemin relatif.
            url_categorie = os.path.join(
                "http://books.toscrape.com/", url_categorie_relative)

            # Parser catégorie par catégorie
            response_categorie = requests.get(url_categorie)
            html_categorie = response_categorie.content
            soup_categorie = BeautifulSoup(html_categorie, "html.parser")

            # Pour trouver la ligne en bas de la page, où est affichée la numérotaion de la page.
            pagination = soup_categorie.find("li", class_="current")

            if pagination == None:
                # s'il y a qu'une page dans la catégorie.
                liste_urls_categories.append(url_categorie)
            else:
                # s'il n'y a plusieurs pages dans la catégorie.
                nb_pages = int(
                    pagination.text.lstrip().rstrip().split(" ")[-1])
                numero_page = 1
                while numero_page <= nb_pages:
                    liste_urls_categories.append(
                        url_categorie.replace("index", f"page-{numero_page}"))
                    numero_page += 1

    else:
        print(f"Echec du scrapping, Status code: {response.status_code}")
    return liste_urls_categories


def infos_livre(url_product_page):
    # Otenir des infos sur chaque livre
    # Cette fonction est appelée par la fonction "scraper_books_to_scrape()""

    # Parser chaque livre.
    response = requests.get(url_product_page)
    html_product_page = response.content
    soup = BeautifulSoup(html_product_page, "html.parser")

    title = soup.h1.string   # Extraction du titre livre.
    # Trouve le tableau d'informations du livre.
    tableau_infos_article = soup.table
    # Extraction de chaque ligne du tableau d'infos.
    infos = tableau_infos_article.find_all("tr")
    upc = infos[0].td.string
    product_type = infos[1].td.string
    price_excl_tax = infos[2].td.string
    price_incl_tax = infos[3].td.string
    tax = infos[4].td.string
    availability = infos[5].td.string
    number_of_reviews = infos[6].td.string
    # Affiche la description du livre.
    product_description = soup.h2.find_next("p").text

    # Isole la barre de navigation en dessus horizontale
    # et trouve le nom de la catégorie.
    barre_denavigation = soup.find("ul", class_="breadcrumb")
    category = barre_denavigation.find_all("li")[-2].a.text

    # Trouve le url de l'image
    url_image_relative = soup.img.attrs["src"]  # Adresse relative de l'image
    # Adresse absolue de l'image
    url_image = urljoin(url_product_page, url_image_relative)

    # Extraction du nombre d'étoiles.
    etoiles = soup.find("p", class_="star-rating").attrs["class"][1]

    # Extraction du nom qui sera attribué à l'image du livre lors du stockage des images.
    nom_image = url_product_page.split("/")[-2]

    # liste des éléments non demandés à titre d'infos
    infos_livres = [upc, title, price_excl_tax, price_incl_tax, availability, category,
                    number_of_reviews, url_image, etoiles, product_description]

    # APPEL DE LA FONCTION "ECRIRE DANS DES FICHIERS CSV"
    ecrire_dans_csv(category=category, infos_livres=infos_livres)

    # APPEL DE LA FONCTION "SAUVEGARDER DES IMAGES"
    sauvegarder_images(url_image=url_image,
                       category=category, nom_image=nom_image)


def ecrire_dans_csv(category, infos_livres):
    # Ecriture dans un fichier csv
    # cette fonction est appelée par la fonction "infos_livre"
    if not os.path.exists("csv"):
        os.makedirs("csv")  # si le dossier csv n'existe pas en créer.

    filename = os.path.join(os.getcwd(), f"csv\{category}.csv")  # Fichier csv
    label_colonnes = ["UPC", "TITRE", "PRICE_EXCL_TAX", "PRICE_INCL_TAX", "AVAILABILITY",
                      "CATEGORY", "NUMBER_OF_REVIEWS", "IMAGE_URL", "ETOILES", "PRODUCT_DESCRIPTION"]
    if not os.path.exists(filename):
        with open(filename, "w", newline="", encoding="utf8") as file:
            writer = csv.writer(file, delimiter=",")
            # Ecririture de l'en-tête de chaque fichier csv.
            writer.writerow(label_colonnes)
            # Ecririture des infos dans chaque fichier csv.
            writer.writerow(infos_livres)
    else:
        with open(filename, "a", newline="", encoding="utf8") as file:
            writer = csv.writer(file, delimiter=",")
            # Inscription des infos de chaque livre dans le fichier csv.
            writer.writerow(infos_livres)


def sauvegarder_images(url_image, category, nom_image):
    # Téléchargement et sauvegarde des images.
    # Cette fonction est appelée par la fonction "infos_livre".
    response = requests.get(url_image)

    # créer le dossier s'il est inexistant.
    if not os.path.exists(f"images\{category}"):
        os.makedirs(f"images\{category}")

    filename = os.path.join(
        os.getcwd(), f"images\{category}\{nom_image}.jpg")  # Fichier image
    with open(filename, "wb") as f:
        # Ecriture de l'image dans un fichier binaire.
        f.write(response.content)


def scraper_books_to_scrape():
    # Permet de récupérer l'adresse de chaque livre.
    # SURTOUT, c'est la FONCTION PRINCIPALE qui permet de scraper le site web.

    # la liste des urls des catégories.
    liste_urls_categories = parcourir_toutes_les_categories()
    liste_urls_product_page = []  # La liste de urls des livres

    for url_categorie in liste_urls_categories:
        # Parser chaque page de la catégorie
        response = requests.get(url_categorie)
        html_de_lapage = response.content
        soup = BeautifulSoup(html_de_lapage, "html.parser")
        # Trouve tous livres sur la page.
        liste_livres_par_page = soup.find_all("article", class_="product_pod")

        for livre in liste_livres_par_page:
            # Parcourir tous les livres pour obtenir leurs urls relatives.
            link = livre.find("a").attrs["href"]
            # Obtenir L'url absolue du livre.
            url_product_page = urljoin(url_categorie, link)
            # la liste de tous urls des livres
            liste_urls_product_page.append(url_product_page)

            # Appel de la fonction "infos_livre()" qui permet de récuperer les infos sur tous les livres
            infos_livre(url_product_page=url_product_page)


scraper_books_to_scrape()

# PROJET BOOK TO SCRAPE (WEB SCRAPER)
# D'abord créer un environement virtuel  avec: python -m venv btscrap
# initialiser un repertory local git avec: git init
# Creer le fichier requirements: pip freeze >requirements.txt

# Avec PIP installer les packages requis
import requests
from bs4 import BeautifulSoup
import csv



#Parcourir toutes les catégories du site web
# def parcourir_toutes_les_categories():
#     url = "http://books.toscrape.com/index.html" # TO DO adresse à saisir
#     response = requests.get(url)
#     html = response.content
#     soup = BeautifulSoup(html, "html.parser")
        
#     liste_categories = soup.find("ul", class_="nav nav-list").find("ul").find_all("li")
#     urls_categories = []
#     for categorie in liste_categories:
#         url_categorie = categorie.a.attrs["href"]
#         urls_categories.append(url_categorie)
#     print(urls_categories)    
#     return urls_categories



#Parcourir toutes les pages du site web
def parcourir_toutes_les_pages():
    pages_urls = []
    for i in range(1, 51):# TO DO : a adapter au nombre de page
        page_url = f"http://books.toscrape.com/catalogue/page-{i}.html"
        pages_urls.append(page_url)
         
    return pages_urls



# Récupérer l'adresse de chaque livre_product_page_url
def recuperer_ladresse_dulivre(page_url):
    response = requests.get(page_url)
    html_delapage = response.content
    soup = BeautifulSoup(html_delapage, "html.parser")
    livres_surlapage = soup.find_all("article", class_="product_pod")
 

    product_page_urls = []
    for livre in livres_surlapage:      
        #Obtenir Les titres. 
        link = livre.find("a").attrs["href"]
        #Obtenir L'url de la page spécifique du livre.
        product_page_url = "http://books.toscrape.com/catalogue/" + link
        product_page_urls.append(product_page_url)
   
    return product_page_urls

    
     
# Otenir des infos sur chaque livre
def infos_chaque_livre():
    product_page_urls = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    response = requests.get(product_page_urls)
    html_pagelivre =  response.content                                                                                                                       
    soup = BeautifulSoup(html_pagelivre, "html.parser")

    # Le contenu de la page entière d'un seul article(livre)
    page_livrecontenu = soup.find("article", class_="product_page")
    title = page_livrecontenu.find("h1").string         
       
    tableau_infos_article = soup.find("table")
    liste_des_lignes = tableau_infos_article.find_all("tr")
    for ligne in liste_des_lignes:
        upc = liste_des_lignes[0].td.string
        product_type = liste_des_lignes[1].td.string
        price_excl_tax = liste_des_lignes[2].td.string
        price_incl_tax = liste_des_lignes[3].td.string
        tax = liste_des_lignes[4].td.string
        availability = liste_des_lignes[5].td.string
        number_of_reviews = liste_des_lignes[6].td.string

    product_description_titre = page_livrecontenu.find(id="product_description")
    product_description = product_description_titre.find_next().find_next().text

    barre_denavigation = soup.find("ul", class_="breadcrumb")
    category =barre_denavigation.find_all("li")[2].find("a").text

    image_url = soup.find("div", class_="item active").img.attrs["src"]
    
    etoiles = page_livrecontenu.find("p", class_="star-rating Three").attrs["class"][1]
   
  
       
    infos_livres =[upc, title, price_excl_tax, price_incl_tax, availability, category, number_of_reviews, image_url, etoiles, product_description]
 
    return infos_livres



# Ecriture dans un fichier csv    
def ecrire_dans_csv(infos_livres):
    with open("Book to scrape.cvs", "w",newline="", encoding="utf8") as file:
        label_colonnes =["UPC", "TITRE", "PRICE_EXCL_TAX", "PRICE_INCL_TAX", "AVAILABILITY", "CATEGORY", "NUMBER_OF_REVIEWS", "IMAGE_URL", "ETOILES", "PRODUCT_DESCRIPTION"]
        writer = csv.writer(file)
        writer.writerow(label_colonnes)
        writer.writerow(infos_livres)






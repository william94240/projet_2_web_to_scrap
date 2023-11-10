# PROJET BOOK TO SCRAPE (WEB SCRAPER)
# D'abord créer un environement virtuel  avec: python -m venv btscrap
# initialiser un repertory local git avec: git init
# Creer le fichier requirements: pip freeze >requirements.txt :Redirection sur requirements.txt
# Dans .gitignore exclure: les fichiers del'environement virtuel, lse fichiers CSV,
 

# Avec PIP installer les packages requis
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin



#Parcourir toutes les catégories du site web
def parcourir_toutes_les_categories():
    url = "http://books.toscrape.com/index.html" # TO DO: adresse à saisir
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
        
    liste_categories = soup.find("ul", class_="nav nav-list").ul.find_all("li")

    liste_urls_categories = []

    for categorie in liste_categories:
        url_categorie_partie = categorie.a.attrs["href"]
        url_categorie_complet = "http://books.toscrape.com/" +  url_categorie_partie           
        
        try:
            response_categorie = requests.get(url_categorie_complet)
            html_categorie = response_categorie.content
            soup_categorie = BeautifulSoup(html_categorie, "html.parser")
            nombre_pages_de_categorie_str = soup_categorie.find("li", class_="current").text.lstrip().rstrip().split(" ")[-1]
            nombre_pages_de_categorie_int = int(nombre_pages_de_categorie_str)

            if nombre_pages_de_categorie_str != "":
                liste_urls_dans_categories =[]
                numero_page = 1
            
                while numero_page <= nombre_pages_de_categorie_int:                        
                        url_categorie_complet = url_categorie_complet.replace("index",f"page-{numero_page}")
                        liste_urls_dans_categories.append(url_categorie_complet)
                        numero_page += 1

            else:
                pass


        except:
            pass

        liste_urls_categories.append(url_categorie_complet)
        # liste_urls_categories.append(liste_urls_dans_categories)
        
    return  liste_urls_categories      
           
   
        
    

   


# Récupérer l'adresse de chaque livre :product_page_url
def recuperer_ladresse_dechaque_livre():
    liste_urls_categories = parcourir_toutes_les_categories()
    liste_product_page_url =[]
    for url_categorie in liste_urls_categories:
        response = requests.get(url_categorie)
        html_de_lapage = response.content
        soup = BeautifulSoup(html_de_lapage, "html.parser")
        livres_sur_lapage = soup.find_all("article", class_="product_pod")
           
        for livre in livres_sur_lapage:      
            #Obtenir Les titres. 
            link = livre.find("a").attrs["href"]
            #Obtenir L'url de la page spécifique du livre.
            product_page_url = urljoin(url_categorie, link )
            liste_product_page_url.append(product_page_url)

            # Appeler la fonction "infos_chaque_livre()"
            infos_chaque_livre(product_page_url)
    

    
  



     
# Otenir des infos sur chaque livre
def infos_chaque_livre(product_page_url):
    # product_page_urls = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    # product_page_urls = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    response = requests.get(product_page_url)
    html_pagelivre =  response.content                                                                                                                       
    soup = BeautifulSoup(html_pagelivre, "html.parser")

    title = soup.h1.string
    tableau_infos_article = soup.table
    liste_des_lignes = tableau_infos_article.find_all("tr")     
    upc = liste_des_lignes[0].td.string
    product_type = liste_des_lignes[1].td.string
    price_excl_tax = liste_des_lignes[2].td.string
    price_incl_tax = liste_des_lignes[3].td.string
    tax = liste_des_lignes[4].td.string
    availability = liste_des_lignes[5].td.string
    number_of_reviews = liste_des_lignes[6].td.string
    product_description = soup.h2.find_next("p").text    
    barre_denavigation_laterale = soup.find("ul", class_="breadcrumb")
    category = barre_denavigation_laterale.find_all("li")[-2].a.text
    image_url = soup.img.attrs["src"]    
    etoiles = soup.find("p", class_="star-rating").attrs["class"][1]   
       
    infos_livres =[upc, title, price_excl_tax, price_incl_tax, availability, category, number_of_reviews, image_url, etoiles, product_description]

   # Appeller  ecrire_dans_csv
    ecrire_dans_csv(infos_livres)



# Ecriture dans un fichier csv
label_colonnes =["UPC", "TITRE", "PRICE_EXCL_TAX", "PRICE_INCL_TAX", "AVAILABILITY", "CATEGORY", "NUMBER_OF_REVIEWS", "IMAGE_URL", "ETOILES", "PRODUCT_DESCRIPTION"]    
def ecrire_dans_csv(infos_livres):
    with open("Book to scrape.csv", "a",newline="", encoding="utf8") as file:
        writer = csv.writer(file, delimiter =",")
        writer.writerow(label_colonnes)
        writer.writerow(infos_livres)


recuperer_ladresse_dechaque_livre()


# PROJET BOOK TO SCRAPE (WEB SCRAPER)
# D'abord créer un environement virtuel  avec: python -m venv btscrap
# initialiser un repertory local git avec: git init
# Creer le fichier requirements: pip freeze >requirements.txt
# Dans .gitignore exclure: les fichiers del'environement virtuel, lse fichiers CSV,
 

# Avec PIP installer les packages requis
import requests
from bs4 import BeautifulSoup
import csv



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
        liste_urls_categories.append(url_categorie_complet)
        
    return liste_urls_categories
    




# Récupérer l'adresse de chaque livre :product_page_url
def recuperer_ladresse_dechaque_livre():
    liste_urls_categories = parcourir_toutes_les_categories()
    liste_product_page_url =[]
    for url_categorie in liste_urls_categories:
        response = requests.get(url_categorie)
        html_delapage = response.content
        soup = BeautifulSoup(html_delapage, "html.parser")
        livres_sur_lapage = soup.find_all("article", class_="product_pod")
           
        for livre in livres_sur_lapage:      
            #Obtenir Les titres. 
            link = livre.find("a").attrs["href"]
            #Obtenir L'url de la page spécifique du livre.
            product_page_url = "http://books.toscrape.com/catalogue/" + link
            liste_product_page_url.append(product_page_url)
    return  liste_product_page_url      
    
         

  
liste_product_page_url =recuperer_ladresse_dechaque_livre()
print(liste_product_page_url)
print(len(liste_product_page_url))


 
     
# Otenir des infos sur chaque livre
def infos_chaque_livre():
    product_page_urls = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
   
    response = requests.get(product_page_urls)
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
def ecrire_dans_csv(infos_livres):
    with open("Book to scrape.cvs", "w",newline="", encoding="utf8") as file:
        label_colonnes =["UPC", "TITRE", "PRICE_EXCL_TAX", "PRICE_INCL_TAX", "AVAILABILITY", "CATEGORY", "NUMBER_OF_REVIEWS", "IMAGE_URL", "ETOILES", "PRODUCT_DESCRIPTION"]
        writer = csv.writer(file)
        writer.writerow(label_colonnes)
        writer.writerow(infos_livres)



# infos_chaque_livre()



# PROJET BOOK TO SCRAPE (WEB SCRAPER)
# D'abord créer un environement virtuel  avec: python -m venv btscrap
# initialiser un repertory local git
# Creer le fichier requirements: pip freeze >requirements.txt

# Avec PIP installer les packages requis
import requests
from bs4 import BeautifulSoup
import pandas
import csv



#Consulter toutes les pages du site web
# def parcourir_toutes_les_pages():
#     numero_page = 1
#     urls = []
    
#     for i in range(50):
#         page = f"https://books.toscrape.com/catalogue/page-{numero_page}.html"
#         numero_page += 1
#         urls.append(page)
    
#     return urls


#Récupérer les titres de chaque livre
# def recuperer_titres_livres():
#     url = "hts://books.toscrape.com/catalogue/page-1.html"
#     response = requests.get(url)
#     code_source_page = response.content
#     soup = BeautifulSoup(code_source_page, "html.parser")
#     livres = soup.find_all("article", class_="product_pod")

#     titres = []
#     for livre in livres:      
#         #Obtenir Les titres. 
#         image = livre.find("img", class_="thumbnail")
#         titre = image.attrs["alt"]
#         titres.append(titre)
#         print(titres)
#     return titres

        
        

# Otenir des infos sur chaque article(livre)
def infos_chaque_article():
    page_livre = f"http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    response = requests.get(page_livre)
    code_source_page_article = response.content
    soup = BeautifulSoup(code_source_page_article, "html.parser")

    # Le contenu de la page entière d'un seul article(livre)
    page_contenu = soup.find("article", class_="product_page")
    
    title = page_contenu.find("h1").string
    etoiles = page_contenu.find("p", class_="star-rating Three").attrs["class"][1]
    product_description_gdparent = page_contenu.find(id="product_description")
    product_description = product_description_gdparent.find_next().find_next().text
       
    tableau = soup.find("table")
    liste_des_lignes = tableau.find_all("tr")
    for ligne in liste_des_lignes:
        upc = liste_des_lignes[0].td.string
        product_type = liste_des_lignes[1].td.string
        price_excl_tax = liste_des_lignes[2].td.string
        price_incl_tax = liste_des_lignes[3].td.string
        tax = liste_des_lignes[4].td.string
        availability = liste_des_lignes[5].td.string
        number_of_reviews = liste_des_lignes[6].td.string

       

        
        print(title, "\n", upc, "\n",  product_type, "\n", price_excl_tax, "\n", price_incl_tax, "\n", tax, "\n", availability, "\n", number_of_reviews)
        
  


infos_chaque_article() 
      










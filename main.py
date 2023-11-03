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




#Récupérer l'adresse de chaque livre (product_page_url)
def recuperer_ladresse_dulivre(page_url):
    response = requests.get(page_url)
    code_source_delapage = response.content
    soup = BeautifulSoup(code_source_delapage, "html.parser")
    livres_surlapage = soup.find_all("article", class_="product_pod")
 

    product_page_urls = []
    for livre in livres_surlapage:      
        #Obtenir Les titres. 
        link = livre.find("a")["href"]
        #Obtenir L'url de la page spécifique du livre.
        product_page_url = "http://books.toscrape.com/catalogue/" + link
        product_page_urls.append(product_page_url)
   
    return product_page_urls




        

# Otenir des infos sur chaque livre
def infos_chaque_livre(product_page_urls):
    product_page_urls = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    response = requests.get(product_page_urls)
    codesource_pagelivre =  response.content                                                                                                                       
    soup = BeautifulSoup(codesource_pagelivre, "html.parser")

    # Le contenu de la page entière d'un seul article(livre)
    page_livrecontenu = soup.find("article", class_="product_page")
    
    title = page_livrecontenu.find("h1").string
    etoiles = page_livrecontenu.find("p", class_="star-rating Three").attrs["class"][1]
    product_description_titre = page_livrecontenu.find(id="product_description")
    product_description = product_description_titre.find_next().find_next().text

    barre_denavigation = soup.find("ul", class_="breadcrumb")
    category =barre_denavigation.find_all("li")[2].find("a").text

    image_url = soup.find("div", class_="item active").img["src"]
    
       
    tableau = soup.find("table")
    lignes_dutableau = tableau.find_all("tr")
    for ligne in lignes_dutableau:
        upc = lignes_dutableau[0].td.string
        product_type = lignes_dutableau[1].td.string
        price_excl_tax = lignes_dutableau[2].td.string
        price_incl_tax = lignes_dutableau[3].td.string
        tax = lignes_dutableau[4].td.string
        availability = lignes_dutableau[5].td.string
        number_of_reviews = lignes_dutableau[6].td.string

       

        
        
    print("upc: ", upc)    
    print("title: ", title)    
    print("price_excl_tax: ", price_excl_tax)    
    print("price_incl_tax: ", price_incl_tax)    
    print("availability: ", availability)    
    print("product_description: ", product_description)    
    print("category: ", category)    
    print("number_of_reviews: ", number_of_reviews)    
    print("image_url: ", image_url)    
    
  
    return upc, title, price_excl_tax, price_incl_tax, availability, product_description, category, number_of_reviews, image_url

      
page_url = "http://books.toscrape.com/index.html"

parcourir_toutes_les_pages()
recuperer_ladresse_dulivre(page_url)






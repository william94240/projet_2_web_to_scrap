# PROJET BOOK TO SCRAPE (WEB SCRAPER)
# D'abord créer un environement virtuel  avec: python -m venv btscrap
# initialiser un repertory local git avec: git init
# Creer le fichier requirements: pip freeze >requirements.txt :Redirection sur requirements.txt
# Dans .gitignore exclure: les fichiers de l'environement virtuel, les fichiers CSV et images,
 

# Avec PIP installer les packages requis
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os



#Parcourir toutes les catégories du site web
def parcourir_toutes_les_categories():
    url = "http://books.toscrape.com/index.html" # TO DO: adresse à saisir
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
        
    liste_categories = soup.find("ul", class_="nav nav-list").ul.find_all("li")
    liste_urls_categories =[]
    for categorie in liste_categories:
        url_categorie_partie = categorie.a.attrs["href"]
        url_categorie = os.path.join("http://books.toscrape.com/", url_categorie_partie)               
        
        response_categorie = requests.get(url_categorie)
        html_categorie = response_categorie.content
        soup_categorie = BeautifulSoup(html_categorie, "html.parser")
        pagination = soup_categorie.find("li", class_="current")
        
        if pagination == None:
            # nb_pages = 1
            liste_urls_categories.append(url_categorie)
        else:
            nb_pages = int(pagination.text.lstrip().rstrip().split(" ")[-1])
        
            numero_page = 1

            while numero_page <= nb_pages:                        
                liste_urls_categories.append(url_categorie.replace("index",f"page-{numero_page}"))
                numero_page += 1            
                
    

    return liste_urls_categories         
      



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
            # Obtenir Les titres. 
            link = livre.find("a").attrs["href"]
            # Obtenir L'url de la page spécifique du livre.
            product_page_url = urljoin(url_categorie, link )
            liste_product_page_url.append(product_page_url)

            # Recuperer les infos sur tous les livres
            infos_livre(param = product_page_url)

   





# Otenir des infos sur chaque livre
def infos_livre(param):
    response = requests.get(param)
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
    barre_denavigation = soup.find("ul", class_="breadcrumb")
    category = barre_denavigation.find_all("li")[-2].a.text
    image_url_relative = soup.img.attrs["src"]
    image_url = urljoin(param,image_url_relative )   
    etoiles = soup.find("p", class_="star-rating").attrs["class"][1]   
       
    infos_livres =[upc, title, price_excl_tax, price_incl_tax, availability, category, number_of_reviews, image_url, etoiles, product_description]
    

    # ECRIRE DANS DES FICHIERS CSV
    ecrire_dans_csv(param_1=category , param_2=infos_livres)

    # SAUVEGARDER DES IMAGES
    # sauvegarder_images(param_3=image_url, param_4 = category, param_5 = title)







# Ecriture dans un fichier csv(cette fonction est appelée par "infos_livre)
def ecrire_dans_csv(param_1, param_2):
    
    if not os.path.exists("csv"):
        os.makedirs("csv")
    # os.chdir("csv")    
    filename = os.path.join(os.getcwd(), f"./csv/{param_1}.csv")
    label_colonnes =["UPC", "TITRE", "PRICE_EXCL_TAX", "PRICE_INCL_TAX", "AVAILABILITY", "CATEGORY", "NUMBER_OF_REVIEWS", "IMAGE_URL", "ETOILES", "PRODUCT_DESCRIPTION"]
    with open(filename, "a",newline="", encoding="utf8") as file:
        writer = csv.writer(file, delimiter =",")
        if not os.path.exists(filename):
            writer.writerow(label_colonnes)
        else:
            writer.writerow(param_2)




# Recuperation des images.
def sauvegarder_images(param_3, param_4,param_5):
    response = requests.get(param_3)
    image_dir = os.path.join(os.getcwd(), f"images/{param_4}")
    # print(image_dir)
       
       
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)    

    os.chdir(image_dir)
         
    with open(f"{param_5}.jpg", "wb") as f:         
        f.write(response.content)

# sauvegarder_images()

    


recuperer_ladresse_dechaque_livre()


from bs4 import BeautifulSoup
import requests
import os

script_directory = os.path.dirname(os.path.abspath(__file__))

nom_serie="riv_emergents"

# Étape 1 : Lire le fichier .txt
with open(script_directory+'\\'+nom_serie+'.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Étape 2 : Analyser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

classes=["img-fluid","card","lazy","corner-radial"]

# Étape 3 : Extraire les liens (par exemple, tous les liens <a>)
div = soup.find_all('img',class_=classes)

div=[d for d in div if ((not "transparent-picture" in d.get('class',[])) and ("/images/sets" in d.get("src",[])))]

noms=[" ".join(d.get("alt",[]).split(" ")[:-1]) for d in div]
liens=[(d.get("src",[]),d.get("src",[]).split("/")[-1]) for d in div]


import subprocess

def telecharger_image(url, emplacement):
    try:
        # Construire la commande curl
        commande = ['curl', '-o', emplacement, url]
        
        # Exécuter la commande
        result = subprocess.run(commande, capture_output=True, text=True)
        
        # Vérifier si la commande a réussi
        if result.returncode == 0:
            print(f'Image téléchargée avec succès : {emplacement}')
        else:
            print(f'Erreur lors du téléchargement de l\'image : {result.stderr}')
    except Exception as e:
        print(f'Une exception s\'est produite : {e}')

for img in liens:
    telecharger_image(img[0],script_directory+"\\"+nom_serie+"\\"+img[1])

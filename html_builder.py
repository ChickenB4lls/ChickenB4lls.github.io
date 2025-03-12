import os

script_directory = os.path.dirname(os.path.abspath(__file__))

fichier_html = 'index.html'

dossiers = [d for d in os.listdir(script_directory) if os.path.isdir(os.path.join(script_directory, d))]

# Récupérer la liste des fichiers dans le dossier
images=[]
for d in dossiers:
    images+=[d+"\\"+f for f in os.listdir(script_directory+"\\"+d) if f.endswith(('.jpg'))]


# Commencer à construire le contenu HTML
html_content = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Collection de ChickenB4lls</title>
    <style>
        .corner-radial {border-radius: 8px;}
    </style>
</head>
<body>'''


# Ajouter chaque image au contenu HTML
for image in images:
    html_content += f'        <img src="{image}" alt="{image}" class="corner-radial">\n'

# Terminer le contenu HTML
html_content += '''
</body>
</html>
'''

# Écrire le contenu HTML dans le fichier
with open(script_directory+"\\"+fichier_html, 'w') as f:
    f.write(html_content)

#print(f'Fichier HTML généré : {fichier_html}')
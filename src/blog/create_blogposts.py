# -*- coding: utf-8 -*-


"""
Ces lignes de code doivent être lancées à l'intérieur d'un interpréteur Python dans le contexte de Django
Vous pouvez lancer cet interpréteur avec la commande "python manage.py shell"
Une fois à l'intérieur de l'interpréteur, importez le modèle BlogPost.
"""

import json

chemin = "blog/blog_blogpost.json"

with open(chemin, "r") as f:
    data = json.load(f)
    
for bp in data:
    BlogPost.objects.create(title=bp["title"],
                            slug=bp["slug"],
                            published=bp["published"],
                            description=bp["description"],
                            date=bp["date"])

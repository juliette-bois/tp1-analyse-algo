# INFO704 - tp1-analyse-algo

---------

L'objectif du TP est de trouver un ordre de livraison des cartes postales qui minimise la distance effectuée par le drone de livraison.

Chaque jour, vous chargez votre drone avec des cartes postales qui lui sont assignées et l’envoyez effectuer les livraisons. 
Une fois toutes les cartes livrées, le drone doit rentrer à la base.
La localisation de chacune des boîtes aux lettres est donnée par deux coordonnées. Des exemples d’entrées sont
données dans le dossier `examples`. 
La première ligne correspond aux coordonnées de la base, les lignes suivantes aux coordonnées des adresses à livrer.

### Introduction
J'ai utilisé le langage Python.

**Comment installer le projet ?**    
A la racine du projet, vous pouvez lancer les commandes suivantes dans votre terminal afin d'installer les dépendances nécessaires.
```
# PuLP : https://pypi.org/project/PuLP/
pip install PuLP
```

Le dossier `src` contient toutes les sources de mes programmes.
Le dossier `examples` contient des exemples d’entrées de coordonnées.

**Comment lancer le programme ?**
```
Question 1 : python3 src/exo1.py examples/cities10
Question 2 (environ 21 secondes d'exécution) : python3 src/exo2.py examples/cities10
Question 3 : python3 src/exo3.py examples/cities10
Question 4 : python3 src/exo4.py examples/cities10
```
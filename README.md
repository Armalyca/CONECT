# **Projet CONECT : Récupération des données**

Les objectifs précis de ce projet sont décrits dans le document synopsis.pdf.

Ce README permet de décrire l'utilisation du tweet_scraper.py, si l'on veut l'utiliser directement dans un terminal.



## Prérequis
- Python 3.5/3.6
- `pip3 install -r requirements.txt`

Ne pas oublier d'utiliser la commande ```$ mongod``` pour démarrer MongoDB.

## Options
Commande|Utilisation
-------|-----------
`-u`|Utilisateur dont on veut récupérer les Tweets.
`-s`|Rechercher des Tweets contenant ce mot ou cette phrase.
`-g`|Rechercher des Tweets géocodés, format de l'arguement : lat,lon,rayon(km ou mi).
`-l`|Rechercher des Tweets dans une langue.
`-test`|Afficher les résultats directement dans le terminal(O ou N).
`--year`|Rechercher des Tweets depuis l'année spécifiée.
`--since`|Rechercher des Tweets depuis la date spécifiée (ex: 2017-12-27).
`--until`|Rechercher des Tweets jusqu'à la date spécifiée (ex: 2017-12-27).
`--fruit`|Afficher les 'low-hanging-fruit' Tweets (pouvant contenir des informations sensibles).
`--verified`|Afficher seulement les Tweets d'utilisateurs verifiés (utilisé avec -s).
`--userid`|Recherche par user id.
`--limit`|Limiter le nombre de Tweets scrapés (multiple de 20).
`--count`|Afficher le nombre de Tweets scrapés.
`--dbname`|Nommer la BDD (CONECT par défaut).


## Remerciement
Merci à Haccer pour le projet https://github.com/haccer/twint sur lequel se base ce script.

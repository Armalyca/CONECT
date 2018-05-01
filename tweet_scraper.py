#!/usr/bin/python3
from bs4 import BeautifulSoup
from time import gmtime, strftime
import argparse
import aiohttp
import asyncio
import async_timeout
import contextlib
import datetime
import hashlib
import json
import re
import sys
import pymongo
from pymongo import MongoClient
import pdb #pour le debug à retirer


class RecycleObject(object):
    def write(self, junk): pass

@contextlib.contextmanager
def nostdout():
    savestdout = sys.stdout
    sys.stdout = RecycleObject()
    yield
    sys.stdout = savestdout

def initdb(db):
    try:
        '''
        On ajoute un document à chaque collection pour les initialiser.
        '''
        client = MongoClient()
        conn = client[db] #connecteur à la BDD
        conn.users.insert_one({"username" : 'init_username_ignore'})
        conn.tweets.insert_one({"tweetid" : 'init_tweet_ignore'})
        return conn
    except:
        Error("Erreur 500", "Impossible d'initialiser la BDD.")




async def getUrl(init):
    '''
    Choix de l'URL
    On utilise la position des Tweets dans le résultat de la recherche avancé de
    Twitter pour itérer à travers le Tweets d'un utilisateur ou de la recherche.

    Cette section définit si c'est la première requete URL ou non, et crée un
    URL selon les paramètres de recherche.

    On fait une recherche sur Twitter en anglais "lang=en" pour que les timestamp des Tweets soient au format jj-mm-aa

    Renvoie l'URL complet.
    '''
    if init == -1:
        url = "https://twitter.com/search?f=tweets&vertical=default&lang=en&q=" #première requête
    else:
        url = "https://twitter.com/i/search/timeline?f=tweets&vertical=default"
        url+= "&lang=en&include_available_features=1&include_entities=1&reset_"
        url+= "error_state=false&src=typd&max_position={}&q=".format(init)

    if arg.u != None:
        url+= "from%3A{0.u}".format(arg)
    if arg.g != None:
        arg.g = arg.g.replace(" ", "")
        url+= "geocode%3A{0.g}".format(arg)
    if arg.s != None:
        arg.s = arg.s.replace(" ", "%20").replace("#", "%23")
        url+= "%20{0.s}".format(arg)
    if arg.year != None:
        url+= "%20until%3A{0.year}-1-1".format(arg)
    if arg.since != None:
        url+= "%20since%3A{0.since}".format(arg)
    if arg.until != None:
        url+= "%20until%3A{0.until}".format(arg)
    if arg.fruit:
        url+= "%20myspace.com%20OR%20last.fm%20OR"
        url+= "%20mail%20OR%20email%20OR%20gmail%20OR%20e-mail"
        url+= "%20OR%20phone%20OR%20call%20me%20OR%20text%20me"
        url+= "%20OR%20keybase"
    if arg.verified:
        url+= "%20filter%3Averified"
    if arg.l:
        url+= "%3Fl={0.l}".format(arg)

    return url

async def fetch(session, url):
    '''
    Requête aiohttp avec une expiration de 30 secondes.
    '''
    with async_timeout.timeout(30):
        async with session.get(url) as response:
            return await response.text()

async def initial(response):
    '''
    Parsing de la première réponse et récupération de l'ID de position.
    '''
    soup = BeautifulSoup(response, "html.parser")
    feed = soup.find_all("li", "js-stream-item")
    init = "TWEET-{}-{}".format(feed[-1]["data-item-id"], feed[0]["data-item-id"])

    return feed, init

async def cont(response):
    '''
    Parsing de la réponse en json et récupération de l'ID de position.
    '''
    json_response = json.loads(response)
    html = json_response["items_html"]
    soup = BeautifulSoup(html, "html.parser")
    feed = soup.find_all("li", "js-stream-item")
    split = json_response["min_position"].split("-")
    split[1] = feed[-1]["data-item-id"]
    init = "-".join(split)

    return feed, init

async def getFeed(init):
    '''
    Choix du type de parsing:
    Responses from requests with the position id's are JSON,
    so this section decides whether this is an initial request
    or not to use the approriate response reading for parsing
    with BeautifulSoup4.

    Renvoie le html des Tweets et leur ID de position.
    '''
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        response = await fetch(session, await getUrl(init))
    feed = []
    try:
        if init == -1:
            feed, init = await initial(response)
        else:
            feed, init = await cont(response)
    except:
        pass

    return feed, init

async def outTweet(tweet):

    tweetid = tweet["data-item-id"]

    # On formate la date et le timestamp à la Française.
    datestamp = tweet.find("a", "tweet-timestamp")["title"].rpartition(" - ")[-1]
    d = datetime.datetime.strptime(datestamp, "%d %b %Y")
    date = d.strftime("%d-%m-%Y")
    timestamp = str(datetime.timedelta(seconds=int(tweet.find("span", "_timestamp")["data-time"]))).rpartition(", ")[-1]
    t = datetime.datetime.strptime(timestamp, "%H:%M:%S")
    time = t.strftime("%H:%M:%S")

    # On enlève le @ dans le nom d'utilisateur.
    username = tweet.find("span", "username").text.replace("@", "")
    timezone = strftime("%Z", gmtime())

    # On remplace tous les emoticons par leur nom pour qu'ils soient inclut dans le tweet.
    for img in tweet.findAll("img", "Emoji Emoji--forText"):
        img.replaceWith("<%s>" % img['aria-label'])

    # On retourne tout le texte sur une ligne,un peu de mise en forme.
    text = tweet.find("p", "tweet-text").text.replace("\n", "").replace("http", " http").replace("pic.twitter", " pic.twitter")

    # Regex pour récupérer les hashtags.
    hashtags = ",".join(re.findall(r'(?i)\#\w+', text, flags=re.UNICODE))

    # Regex pour récupérer les urls des images.
    imglinks = ",".join(re.findall('pic.twitter.com/(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text))

    # Regex pour récupérer les urls.
    links = ",".join(re.findall('https://(?:[-\w.]|(?:%[\da-fA-F]{2}))+|http://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text))

    # Recherche dans le html des tweets pour isolder le nombre de réponses, retweets et likes.
    replies = tweet.find("span", "ProfileTweet-action--reply u-hiddenVisually").find("span")["data-tweet-stat-count"]
    retweets = tweet.find("span", "ProfileTweet-action--retweet u-hiddenVisually").find("span")["data-tweet-stat-count"]
    likes = tweet.find("span", "ProfileTweet-action--favorite u-hiddenVisually").find("span")["data-tweet-stat-count"]


    try:
        mentions = tweet.find("div", "js-original-tweet")["data-mentions"].split(" ")
        for i in range(len(mentions)):
            mention = "@{}".format(mentions[i])
            if mention not in text:
                text = "{} {}".format(mention, text)
    except:
        pass

    '''
    Insertion des tweets/users et des métadonnées dans la BDD
    '''
    #On vérifie si le tweet n'est pas déjà dans la BDD, sinon on l'ajoute.
    if mydb.tweets.find({"tweetid" : tweetid}).count() == 0:
        mydb.tweets.insert_one({
        "tweetid" : tweetid,
        "date" : date,
        "time" : time,
        "timezone" : timezone,
        "username" : username,
        "text" : text,
        "replies" : replies,
        "likes" : likes,
        "retweets" : retweets,
        "hashtags" : hashtags,
        "imglinks" : imglinks,
        "links" : links})


    #On vérifie si l'utilisateur n'est pas déjà dans la BDD, sinon on l'ajoute.
    #pdb.set_trace()
    if mydb.users.find({"username": username}).count() == 0:
        mydb.users.insert_one({"username" : username})

    if arg.test == 'O':
        output = "\n{} {} {} {} <{}> {}".format(tweetid, date, time, timezone, username, text)
        output+= " | {} replies {} retweets {} likes".format(replies, retweets, likes)
        output+= "\nImage Links: {}".format(imglinks)
        output+= "\nLinks: {}".format(links)
        output+= "\nHashtags: {}".format(hashtags)
        return (output)


async def getTweets(init):
    '''
    Cette fonction utilise le html renvoyé par getFeed()
    et envoie cette info au parser de Tweet et la renvoie.

    Renvoie le file de réponse, si c'est la première itération, et le compte de Tweets.
    '''
    tweets, init = await getFeed(init)
    count = 0
    for tweet in tweets:
        '''
        Certain Tweets sont supprimés pour des raisons de copyright mais sont
        encore visible dans les résultats de recherche. On cherche à éviter ces Tweets.
        '''
        copyright = tweet.find("div","StreamItemContent--withheld")
        if copyright is None:
            count +=1
            print(await outTweet(tweet))

    return tweets, init, count

async def getUsername():
    '''
    Cette fonction permet d'obtenir le nom d'un utilisateur à partir d'un ID d'utilisateur.
    '''
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        r = await fetch(session, "https://twitter.com/intent/user?user_id={0.userid}".format(arg))
    soup = BeautifulSoup(r, "html.parser")
    return soup.find("a", "fn url alternate-context")["href"].replace("/", "")

async def main():
    global mydb

    if arg.dbname:
        print("Insertion dans la BDD: " + str(arg.dbname))
        mydb = initdb(arg.dbname)
        if isinstance(mydb, str):
            print(str)
            sys.exit(1)

    else:
        print("Insertion dans la BDD: " + 'CONECT')
        mydb = initdb('CONECT')
        if isinstance(mydb, str):
            print(str)
            sys.exit(1)



    if arg.userid is not None:
        arg.u = await getUsername()

    feed = [-1]
    init = -1
    num = 0
    while True:
        '''
        Si la réponse de getFeed() à une exception,cela signifie qu'il n'y plus
        d'IDs de position, donc le script a fini.
        '''
        if len(feed) > 0:
            feed, init, count = await getTweets(init)
            num += count
        else:
            break
        if arg.limit is not None and num >= int(arg.limit):
            break


    if arg.count:
        print("Fini: {} Tweets collectés.".format(num))

def Error(error, message):
    print("[-] {}: {}".format(error, message))
    sys.exit(0)

def check():
    if arg.u is not None:
        if arg.verified:
            Error("Arguments Contradictoires", "Utiliser --verified avec -s.")
        if arg.userid:
            Error("Arguments Contradictoires", "--userid et -u ne peuvent être utilisés ensemble.")
    if arg.limit is not None:
        if int(arg.limit)%20 != 0:
            Error("Argument Invalide", "La limite de Tweets scrapés doit être un multiple de 20")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="tweep.py", usage="python3 %(prog)s [options]", description="un scrapper de tweet adapté de tweep.py")
    ap.add_argument("-u", help="Utilisateur dont on veut récupérer les Tweets.")
    ap.add_argument("-s", help="Rechercher des Tweets contenant ce mot ou cette phrase.")
    ap.add_argument("-g", help="Rechercher des Tweets géocodés.")
    ap.add_argument("-l", help="Rechercher des Tweets dans une langue")
    ap.add_argument("-test", help="Afficher les résultats directement dans le terminal(O ou N).")
    ap.add_argument("--year", help="Rechercher des Tweets depuis l'année spécifiée.")
    ap.add_argument("--since", help="Rechercher des Tweets depuis la date spécifiée (ex: 2017-12-27).")
    ap.add_argument("--until", help="Rechercher des Tweets jusqu'à la date spécifiée (ex: 2017-12-27).")
    ap.add_argument("--fruit", help="Afficher les 'low-hanging-fruit' Tweets", action="store_true")
    ap.add_argument("--verified", help="Afficher seulement les Tweets d'utilisateurs verifiés (Utiliser avec -s).", action="store_true")
    ap.add_argument("--userid", help="Twitter user id")
    ap.add_argument("--limit", help="Limiter le nombre de Tweets scrapés (Multiple de 20).")
    ap.add_argument("--count", help="Afficher le nombre de Tweets scrapés.", action="store_true")
    ap.add_argument("--dbname", help="Nommer la BDD (CONECT par défaut).")
    arg = ap.parse_args()

    check()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

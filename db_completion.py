import subprocess
import json
import argparse
import pymongo
from pymongo import MongoClient
import tweepy
import pdb #pour le debug à retirer




def fetch_user(username):
    user = api.get_user(tweetid)
    return user

def complete_users():
    for doc in mydb.users.find():
        if mydb.tweets.find({"username" : (doc["username"]), "completed" : False}).count() == 1:
            try:
                user = fetch_user(doc["username"])

                mydb.users.update_one(
                {"username" : doc["username"]},
                {"$set": {
                            "verified" : user.verified,
                            "followers" : user.followers_count,
                            "location" : user.location,
                            "description" : user.description,
                            "completed" : True
                }})
            except:
                pass




def fetch_tweet(tweetid):
    tweet = api.get_status(tweetid)
    return tweet

def complete_tweets():
    for doc in mydb.tweets.find():
        if mydb.tweets.find({"tweetid" : (doc["tweetid"]), "completed" : False}).count() == 1:
            try:
                tweet = fetch_tweet(int(doc["tweetid"]))

                mydb.tweets.update_one(
                {"tweetid" : tweetid},
                {"$set": {
                            "place" : tweet.place,
                            "coordinates" : tweet.coordinates,
                            "completed" : True
                }})
            except:
                pass






def initdb(db):
    try:
        client = MongoClient()
        conn = client[db] #connecteur à la BDD
        return conn
    except:
        print("Erreur 500", "Impossible d'initialiser la BDD.")

def main():
    consumer_key = 'CONSUMER KEY'
    consumer_secret =  'CONSUMER SECRET'
    access_token = 'ACCESS TOKEN'
    access_secret = 'ACCESS SECRET'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    global api
    api = tweepy.API(auth)


    global mydb
    if arg.dbname:
        mydb = initdb(arg.dbname)
        if isinstance(mydb, str):
            print(str)
            sys.exit(1)
    else:
        mydb = initdb('CONECT')
        if isinstance(mydb, str):
            print(str)
            sys.exit(1)

    complete_users()
    complete_tweets()



if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="tweep.py", usage="python3 %(prog)s [options]")
    ap.add_argument("-dbname", help="Nom de la BDD.")
    arg = ap.parse_args()

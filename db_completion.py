import subprocess
import json
import argparse
import pymongo
from pymongo import MongoClient
import pdb #pour le debug à retirer

def user_into_json(screen_name): #Récupération des données de l'utilisateur au format JSON
    user_id = str(id)
    command = "twurl /1.1/users/show.json?id=" + user_id + " | jq '. | {id: .id_str, name: .name, screen_name: .screen_name, verified: .verified, created_at: .created_at, bio: .description, geo_enabled: .geo_enabled, location: .location, time_zone: .time_zone, lang: .lang, followers_count: .followers_count, statuses_count: .statuses_count}' > user.json"
    output = subprocess.check_output(command, shell = True) #not secure, proposed solution by the python documentation leads to error



#Connection au serveur
def complete_users(db):

    for i in users_list:
        user_into_json(i)

        with open("user.json") as user_json:
            f_user = json.load(user_json)
            #Rajouter l'utilisateur dans la BDD si non présent
            if conn.users.find({"id": f_user['id']}).count() == 0:
                conn.users.insert_one(f_user).inserted_id
                print(i, " : Inséré")
            else:
                print(i, " : Cet utilisateur est déjà présent dans la collection \"users\"")

def tweet_into_json(tweetid):


def complete_tweets(db):




def initdb(db):
    try:
        client = MongoClient()
        conn = client[db] #connecteur à la BDD
        return conn
    except:
        Error("Erreur 500", "Impossible d'initialiser la BDD.")

def main():
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

    complete_users(mydb)
    complete_tweets(mydb)



if __name__ == "__main__":
    ap = argparse.ArgumentParser(prog="tweep.py", usage="python3 %(prog)s [options]")
    ap.add_argument("-dbname", help="Nom de la BDD.")
    arg = ap.parse_args()







client.close()

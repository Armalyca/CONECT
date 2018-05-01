import subprocess
import json
import pymongo
from pymongo import MongoClient

def user_into_json(id): #Récupération des données de l'utilisateur au format JSON
    user_id = str(id)
    command = "twurl /1.1/users/show.json?id=" + user_id + " | jq '. | {id: .id_str, name: .name, screen_name: .screen_name, verified: .verified, created_at: .created_at, bio: .description, geo_enabled: .geo_enabled, location: .location, time_zone: .time_zone, lang: .lang, followers_count: .followers_count, statuses_count: .statuses_count}' > user.json"
    output = subprocess.check_output(command, shell = True) #not secure, proposed solution by the python documentation leads to error



#Connection au serveur
def users_database_feed(users_list):

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


client = MongoClient(host = 'localhost', port = 44444)
conn = client['CONECT']

users_list = [1976143068, 18814998, 4127289801, 18814998]
users_database_feed(users_list) #exemple d'appel

client.close()

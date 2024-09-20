from pymongo import MongoClient
from config import mongo_db_name, mongo_db_link, kai_db_link, kai_db_name


def get_db():
    #To use Mongo, replace kai_db_link with mongo_db_link, the url to your mongo cluster
    client = MongoClient(kai_db_link)

    try:
        #To use Mongo, replace kai_db_name with mongo_db_name, the name of your mongo databasegi
        db = client[kai_db_name]
        yield db
    
    finally: 
        client.close()


    
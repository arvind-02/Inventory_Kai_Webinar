import sys
import os
sys.path.append(os.path.abspath('../'))
from config import kai_db_link, kai_db_name, mongo_db_link, mongo_db_name,db_link, db_name
from pymongo import MongoClient

client = MongoClient(kai_db_link)
db = client[kai_db_name]

mongo_client = MongoClient(mongo_db_link)
mongo_db = mongo_client[mongo_db_name]

kai_collections_drop = ['users', 'products', 'orders']
mongo_collections_drop = ['users', 'products', 'orders']

for collection_name in kai_collections_drop:
    db[collection_name].drop()

for collection_name in mongo_collections_drop:
    mongo_db[collection_name].drop()

print("All collections have been dropped.")

client.close()
mongo_client.close()
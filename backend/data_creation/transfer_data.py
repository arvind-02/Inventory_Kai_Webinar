import sys
import os
sys.path.append(os.path.abspath('../'))
from config import mongo_db_link, mongo_db_name, kai_db_link, kai_db_name
from pymongo import MongoClient
import os
from bson.json_util import dumps, loads


source_client = MongoClient(kai_db_link)
source_db = source_client[kai_db_name]

target_client = MongoClient(mongo_db_link)
target_db = target_client[mongo_db_name]

def transfer_data():
    # Get all collections in the source database
    collections = ['products', 'users', 'orders']

    for collection_name in collections:
        print(f"Transferring collection: {collection_name}")
        
        # Get the source collection
        source_collection = source_db[collection_name]
        
        # Get the target collection
        target_collection = target_db[collection_name]
        
        # Retrieve all documents from the source collection
        documents = source_collection.find()
        
        print("documents retrieved")
        
        target_collection.insert_many(loads(dumps(documents)))


transfer_data()
    
# Close connections
source_client.close()
target_client.close()
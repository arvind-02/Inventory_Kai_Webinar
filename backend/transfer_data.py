from config import db_link, db_name, mongo_db_link, mongo_db_name, kai_db_link, kai_db_name
from pymongo import MongoClient
import os
import ast
from bson import ObjectId
from bson.json_util import dumps, loads
import crud
import schemas
from fastapi import FastAPI, Depends, HTTPException

source_client = MongoClient(kai_db_link)
source_db = source_client[kai_db_name]

target_client = MongoClient(mongo_db_link)
target_db = target_client[mongo_db_name]

def transfer_data():
    # Get all collections in the source database
    collections = ['orders', 'users']

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
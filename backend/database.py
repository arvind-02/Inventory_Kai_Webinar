from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import os
from typing import Generator

mongo_link = os.getenv("MONGO_LINK")
mongo_database = os.getenv("MONGO_DATABASE")


def get_db():
    client = MongoClient(mongo_link)

    try:
        db = client[mongo_database]
        yield db
    
    finally: 
        client.close()


    
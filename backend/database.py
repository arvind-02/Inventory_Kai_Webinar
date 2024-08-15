from pymongo import MongoClient
from config import db_link, db_name


def get_db():
    client = MongoClient(db_link)

    try:
        db = client[db_name]
        yield db
    
    finally: 
        client.close()


    
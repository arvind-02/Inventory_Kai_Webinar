from config import db_link, db_name
from pymongo import MongoClient

client = MongoClient(db_link)
db = client[db_name]
for collection_name in db.list_collection_names():
    db[collection_name].drop()
print("All collections have been dropped.")
client.close()
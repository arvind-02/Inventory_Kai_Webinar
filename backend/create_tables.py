from config import db_link, db_name
from pymongo import MongoClient


client = MongoClient(db_link)
db = client[db_name]

db.create_collection("products",
  columns=[{ 'id': "description_embedding", 'type': "VECTOR(1536) NOT NULL" }],
);

db.command({
    'createIndexes': "products",
    'indexes': [{
        'key': {'description_embedding': 'vector'},
        'name': 'vector_index',
        'kaiSearchOptions': {"index_type":"AUTO", "metric_type": "DOT_PRODUCT", "dimensions": 1536}
    }],
})
client.close()
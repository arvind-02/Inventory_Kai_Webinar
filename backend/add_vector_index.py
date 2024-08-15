from config import db_link, db_name
from pymongo import MongoClient
from pymongo.operations import IndexModel

client = MongoClient(db_link)
db = client[db_name]

db.command({
    'createIndexes': 'products',
    'indexes': [{
        'key': {'description_embedding': 'vector'},
        'name': 'vector_index',
        'kaiIndexOptions': {"index_type":"AUTO", "metric_type": "DOT_PRODUCT", "dimensions": 1536}
    }],
})

print("Index Created")
client.close()
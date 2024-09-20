import sys
import os
sys.path.append(os.path.abspath('../'))
from config import kai_db_link, kai_db_name
from pymongo import MongoClient


client = MongoClient(kai_db_link)
db = client[kai_db_name]

db.create_collection("products",
  columns=[{ 'id': "description_embedding", 'type': "VECTOR(1024) NOT NULL" }],
);

db.command({
    'createIndexes': "products",
    'indexes': [{
        'key': {'description_embedding': 'vector'},
        'name': 'vector_index',
        'kaiSearchOptions': {"index_type":"AUTO", "metric_type": "DOT_PRODUCT", "dimensions": 1024}
    }],
})
client.close()
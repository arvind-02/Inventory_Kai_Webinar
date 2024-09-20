from config import kai_db_link, kai_db_name
from pymongo import MongoClient
from pymongo.operations import IndexModel

client = MongoClient(kai_db_link)
db = client[kai_db_name]

db.command({
    'createIndexes': "products",
    'indexes': [{
        'key': {'description_embedding': 'vector'},
        'name': 'vector_index',
        'kaiSearchOptions': {"index_type":"AUTO", "metric_type": "DOT_PRODUCT", "dimensions": 1024}
    }],
})
print("Index Created")
client.close()


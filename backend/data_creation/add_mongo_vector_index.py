import sys
import os
sys.path.append(os.path.abspath('../'))
from config import mongo_db_link, mongo_db_name
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

mongo_client = MongoClient(mongo_db_link)
mongo_db = mongo_client[mongo_db_name]
mongo_products = mongo_db['products']

vector_index = SearchIndexModel(
  definition={
    "fields": [
      {
        "type": "vector",
        "path": "description_embedding",
        "numDimensions": 1024,
        "similarity": "dotProduct"
      }
    ]
  },
  name="vector_index",
  type="vectorSearch",
)

mongo_products.create_search_index(vector_index)
mongo_client.close()
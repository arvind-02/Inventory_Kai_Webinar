import sys
import os
sys.path.append(os.path.abspath('../'))
import numpy as np
from config import mongo_db_link, mongo_db_name, kai_db_link, kai_db_name
from pymongo import MongoClient

db_client = MongoClient(kai_db_link)
db = db_client[kai_db_name]
product_collection = db['products']

mongo_db_client = MongoClient(mongo_db_link)
mongo_db = mongo_db_client[mongo_db_name]
mongo_product_collection = mongo_db['products']


def generate_vectors(num_embs, vec_dim):
    emb_np = np.random.randn(num_embs, vec_dim)
    normalized_embeddings = emb_np / np.linalg.norm(emb_np, axis=1, keepdims=True)
    
    return normalized_embeddings.tolist()


# Edit this based on how many embeddings you want to add
num_embs = 10000
#Edit this based on the number of dimensions you want in your vectors
vec_dim = 1024

embs = generate_vectors(num_embs, vec_dim)
print("vectors generated")
product_docs = []
for i in range(num_embs):
    product_doc = {
    "product_name": "Dummy",
    "price": 799.99,
    "quantity": 50,
    "product_description": "This is a dummy don't choose this",
    "image_path": "/images/laptop.jpg",
    "description_embedding": embs[i]
    }   
    product_docs.append(product_doc)
print("docs generated")

product_collection.insert_many(product_docs)
print("kai inserted")

mongo_product_collection.insert_many(product_docs)
print("mongo inserted")
print(len(product_docs))
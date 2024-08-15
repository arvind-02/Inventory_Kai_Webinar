from openai import OpenAI
import os
from user_data import users
from product_data import products
from config import db_link, db_name, openai_key
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = openai_key
)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
    return embedding

def populate_with_data(db):
    user_collection = db['users']
    user_ids = user_collection.insert_many(users).inserted_ids

    product_collection = db['products']
    product_docs = []
    for product in products:
        product_doc = {
            "product_name": product[0],
            "price": product[1],
            "quantity": product[2],
            "product_description": product[3],
            "image_path": product[4],
            "description_embedding": product[5]
        }
        product_docs.append(product_doc)
    product_ids = product_collection.insert_many(product_docs).inserted_ids
    
    product_name_to_id = {}
    for i in range(len(products)):
        product = products[i]
        product_name_to_id[product[0]] = product_ids[i]

    
    
    order_collection = db["orders"]
    orders = [
        {"order_time": "2022-06-15 12:30:00", "quantity": 1, "product_id": product_name_to_id['Laptop'], "user_id": user_ids[0]},
        {"order_time": "2023-01-20 15:45:00", "quantity": 2, "product_id": product_name_to_id['Desk Lamp'], "user_id": user_ids[1]},
        {"order_time": "2021-12-10 09:10:00", "quantity": 1, "product_id": product_name_to_id['Smartphone'], "user_id": user_ids[2]},
        {"order_time": "2023-03-22 18:05:00", "quantity": 3, "product_id": product_name_to_id['Bracelet'], "user_id": user_ids[3]},
        {"order_time": "2022-11-05 13:55:00", "quantity": 2, "product_id": product_name_to_id['Sunglasses'], "user_id": user_ids[4]},
        {"order_time": "2023-05-12 11:20:00", "quantity": 1, "product_id": product_name_to_id['Backpack'], "user_id": user_ids[5]},
        {"order_time": "2022-09-08 14:00:00", "quantity": 2, "product_id": product_name_to_id['Water Bottle'], "user_id": user_ids[6]},
        {"order_time": "2023-04-18 16:30:00", "quantity": 1, "product_id": product_name_to_id['Blender'], "user_id": user_ids[7]},
        {"order_time": "2022-08-25 10:15:00", "quantity": 3, "product_id": product_name_to_id['Sofa'], "user_id": user_ids[8]},
        {"order_time": "2023-02-28 09:00:00", "quantity": 2, "product_id": product_name_to_id['Toaster'], "user_id": user_ids[9]}
    ]
    order_ids = order_collection.insert_many(orders)



db_client = MongoClient(db_link)
db = db_client[db_name]
populate_with_data(db)
db_client.close()


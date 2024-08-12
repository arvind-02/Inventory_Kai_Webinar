from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection
from sqlalchemy import text
from bson import ObjectId
from pymongo.database import Database
from openai import OpenAI
import os
from llm import GPTEmailGenerator

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)


def get_user(db: Database, user_id: int):
    return db.users.find_one({"_id": ObjectId(user_id)})

def get_product(db: Database, product_id: int):
    return db.products.find_one({"_id": ObjectId(product_id)})

def get_order(db: Database, order_id: int):
    return db.orders.find_one({"_id": ObjectId(order_id)})

def get_email(prev_product_name, new_product_name, prev_product_description, new_product_description, user_name):
    model = GPTEmailGenerator()
    return model.get_email(prev_product_name, new_product_name, prev_product_description, new_product_description, user_name)

def get_orders(db: Database, skip: int = 0, limit: int = 100):
    order_collection = db["orders"]

    pipeline = [
        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {"$unwind": "$user"},
        {"$unwind": "$product"},
        {"$skip": skip},
        {"$limit": limit},
        {
            "$project": {
                "_id": 1,
                "user_id": 1,
                "product_id": 1,
                "quantity": 1,
                "order_time": 1,
                "user_name": "$user.name",
                "product_name": "$product.product_name",
                "product_description": "$product.product_description",
                "product_price": "$product.price",
                "product_image_path": "$product.image_path"
            }
        }
    ]
    return list(order_collection.aggregate(pipeline))

def get_recommended_product(product_id: str, db: Database):
    prod_obj_id = ObjectId(product_id)
    reference_product = db.products.find_one({"_id": prod_obj_id})
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",  # Replace with your actual index name
                "path": "description_embedding",
                "queryVector": reference_product["description_embedding"],
                "numCandidates": 100,
                "limit": 2
            }
        },
        {
            "$match": {
                "_id": {"$ne": ObjectId(product_id)}  # Exclude the reference product
            }
        },
        {
            "$project": {
                "id": {"$toString": "$_id"},
                "product_name": 1,
                "product_description": 1,
                "image_path": 1,
                "similarity_score": {"$meta": "vectorSearchScore"}
            }
        },
        {
            "$limit": 1
        }
    ]

    result = list(db.products.aggregate(pipeline))
    print(result[0])
    return result[0]



    


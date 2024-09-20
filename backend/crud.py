from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection
from sqlalchemy import text
from bson import ObjectId
from pymongo.database import Database
from openai import OpenAI
import os
from llm import GPTEmailGenerator
from config import openai_key
from datetime import datetime, timedelta
import time
from pymongo.errors import OperationFailure

client = OpenAI(
    api_key = openai_key
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

def get_orders(db: Database, skip: int = 0, limit: int = 30):
    order_collection = db["orders"]
    
    pipeline = [
        {"$sort": {"order_time": -1}},
        {"$limit": limit},
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
        },
        
        
        
    ]
    
    try:
        result = list(order_collection.aggregate(pipeline))
    
    except Exception as e:
        print(e)

    return result

def get_recommended_product(product_id: str, db: Database):
    prod_obj_id = ObjectId(product_id)
    reference_product = db.products.find_one({"_id": prod_obj_id})
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",  
                "path": "description_embedding",
                "queryVector": reference_product["description_embedding"],
                "numCandidates": 100,
                "limit": 2
            }
        },
        {
            "$match": {
                "_id": {"$ne": prod_obj_id}  
            }
        },
        {
            "$project": {
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
    wanted = result[0]
    wanted['_id'] = str(wanted['_id'])
    
    return wanted

def get_user_year_history(user_id:str, db: Database):
    user_obj_id = ObjectId(user_id)
    orders_collection = db['orders']
    last_year = datetime.now() - timedelta(days=365)

    try:
        last_year_result = orders_collection.aggregate([
            {
                '$match': {
                    'user_id': user_obj_id,
                    'order_time': {'$gte': last_year}
                }
            },
            {
                '$lookup': {
                    'from': 'products',
                    'localField': 'product_id',
                    'foreignField': '_id',
                    'as': 'product'
                }
            },
            {
                '$project': {
                    'total_spent': {'$multiply': ['$quantity', {'$arrayElemAt': ['$product.price', 0]}]},
                    'total_quantity': '$quantity'
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_orders_last_year': {'$count': {}},
                    'total_amount_spent_last_year': {'$sum': '$total_spent'},
                    'total_quantity_ordered_last_year': {'$sum': '$total_quantity'}
                }
            }
        ]).next()
        
    except StopIteration:
        
        last_year_result = {
            'total_orders_last_year': 0,
            'total_amount_spent_last_year': 0.0,
            'total_quantity_ordered_last_year': 0,
            'execution_time': -1
        }

    return last_year_result

def get_user_month_history(user_id:str, db: Database):
    user_obj_id = ObjectId(user_id)
    orders_collection = db['orders']

    last_month = datetime.now() - timedelta(days=30)
    
    try:
        last_month_result = orders_collection.aggregate([
            {
                '$match': {
                    'user_id': user_obj_id,
                    'order_time': {'$gte': last_month}
                }
            },
            {
                '$lookup': {
                    'from': 'products',
                    'localField': 'product_id',
                    'foreignField': '_id',
                    'as': 'product'
                }
            },
            {
                '$project': {
                    'total_spent': {'$multiply': ['$quantity', {'$arrayElemAt': ['$product.price', 0]}]},
                    'total_quantity': '$quantity'
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_orders_last_month': {'$count': {}},
                    'total_amount_spent_last_month': {'$sum': '$total_spent'},
                    'total_quantity_ordered_last_month': {'$sum': '$total_quantity'}
                }
            }
        ]).next()

        
    except StopIteration:
        
        last_month_result = {
            'total_orders_last_month': 0,
            'total_amount_spent_last_month': 0.0,
            'total_quantity_ordered_last_month': 0
        }
    return last_month_result


def get_product_year_history(product_id:str, db: Database):
    product_obj_id = ObjectId(product_id)
    orders_collection = db['orders']
    products_collection = db['products']
    last_year = datetime.now() - timedelta(days=365)

    try:
        last_year_result = orders_collection.aggregate([
            {
                '$match': {
                    'product_id': product_obj_id,
                    'order_time': {'$gte': last_year}
                }
            },
            {
                '$project': {
                    'total_quantity': '$quantity'
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_orders_last_year': {'$count': {}},
                    'total_quantity_ordered_last_year': {'$sum': '$total_quantity'}
                }
            }
        ]).next()

        product = products_collection.find_one({'_id': product_obj_id})
        
        product_price = product['price'] if product else 0
        last_year_result['total_amount_spent_last_year'] = product_price * last_year_result['total_quantity_ordered_last_year']
        
    except StopIteration:
        
        last_year_result = {
            'total_orders_last_year': 0,
            'total_amount_spent_last_year': 0.0,
            'total_quantity_ordered_last_year': 0
        }

    return last_year_result

def get_product_month_history(product_id:str, db: Database):
    product_obj_id = ObjectId(product_id)
    orders_collection = db['orders']
    products_collection = db['products']
    last_month = datetime.now() - timedelta(days=30)

    try:
        last_month_result = orders_collection.aggregate([
            {
                '$match': {
                    'product_id': product_obj_id,
                    'order_time': {'$gte': last_month}
                }
            },
            {
                '$project': {
                    'total_quantity': '$quantity'
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_orders_last_month': {'$count': {}},
                    'total_quantity_ordered_last_month': {'$sum': '$total_quantity'}
                }
            }
        ]).next()

        product = products_collection.find_one({'_id': product_obj_id})
        product_price = product['price'] if product else 0
        last_month_result['total_amount_spent_last_month'] = product_price * last_month_result['total_quantity_ordered_last_month']
        
    except StopIteration:
        
        last_month_result = {
            'total_orders_last_month': 0,
            'total_amount_spent_last_month': 0.0,
            'total_quantity_ordered_last_month': 0
        }

    return last_month_result
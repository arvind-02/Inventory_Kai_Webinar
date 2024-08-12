from bson import ObjectId
from datetime import datetime

user_schema = {
    "name": str,
    "username": str,
}

product_schema = {
    "product_name": str,
    "product_description": str,
    "price": float,
    "quantity": int,
    "image_path": str,
    "description_embedding": list
}

order_schema = {
    "user_id": ObjectId,
    "product_id": ObjectId,  # List of dicts with product_id and quantity
    "quantity": int,
    "order_time": datetime
}



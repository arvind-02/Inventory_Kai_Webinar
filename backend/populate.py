from openai import OpenAI
import os
from user_data import users
from product_data import products
from database import mongo_link, mongo_database
from pymongo import MongoClient


client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
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

'''
def populate_with_data(db: Session, connection: Connection):
    db.add_all(users)
    db.commit()

    
    for product in products:
        result = connection.execute(
            text("""
                INSERT INTO products (product_name, price, quantity, product_description, image_path, description_embedding)
                VALUES (:product_name, :price, :quantity, :product_description, :image_path, :description_embedding)
            """),
            {
                "product_name": product[0],
                "price": product[1],
                "quantity": product[2],
                "product_description": product[3],
                "image_path": product[4],
                "description_embedding": product[5]
            }
            

        )

    product_ids = {}   
    result = connection.execute(text("SELECT id, product_name FROM products")).fetchall()
    
    for row in result:
       product_ids[row[1]] = row[0]
        
    connection.commit()

    orders = [
        Order(order_time="2022-06-15 12:30:00", quantity=1, product_id=product_ids['Laptop'], user_id=users[0].id),
        Order(order_time="2023-01-20 15:45:00", quantity=2, product_id=product_ids['Desk Lamp'], user_id=users[1].id),
        Order(order_time="2021-12-10 09:10:00", quantity=1, product_id=product_ids['Smartphone'], user_id=users[2].id),
        Order(order_time="2023-03-22 18:05:00", quantity=3, product_id=product_ids['Bracelet'], user_id=users[3].id),
        Order(order_time="2022-11-05 13:55:00", quantity=2, product_id=product_ids['Sunglasses'], user_id=users[4].id),
        Order(order_time="2023-05-12 11:20:00", quantity=1, product_id=product_ids['Backpack'], user_id=users[5].id),
        Order(order_time="2022-09-08 14:00:00", quantity=2, product_id=product_ids['Water Bottle'], user_id=users[6].id),
        Order(order_time="2023-04-18 16:30:00", quantity=1, product_id=product_ids['Blender'], user_id=users[7].id),
        Order(order_time="2022-08-25 10:15:00", quantity=3, product_id=product_ids['Sofa'], user_id=users[8].id),
        Order(order_time="2023-02-28 09:00:00", quantity=2, product_id=product_ids['Toaster'], user_id=users[9].id)
    ]
    db.add_all(orders)
    db.commit()

'''

client = MongoClient(mongo_link)
db = client[mongo_database]
populate_with_data(db)
client.close()


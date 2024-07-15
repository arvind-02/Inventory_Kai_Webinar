from faker import Faker
from sqlalchemy import BigInteger
from sqlalchemy.orm import Session
from models import User, Product, Order
from database import SessionLocal
import random
from openai import OpenAI
import os
import numpy as np

client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)


descriptions = {"Laptop": '''Discover the ultimate in portable computing with our sleek Laptop.
                 Featuring a powerful processor and expansive storage, it's your perfect companion for work and play,
                 whether you're at home or on the move.''',
                "Smartphone": '''Revolutionize your connectivity with our cutting-edge Smartphone.
                Boasting lightning-fast performance, a vibrant touchscreen, and stunning camera capabilities,
                    it keeps you connected and entertained wherever you go. ''',
                "Headphones": ''' Immerse yourself in superior sound quality with our premium Headphones. 
                Featuring advanced noise-canceling technology and luxurious comfort, 
                they're crafted for audiophiles and professionals seeking unparalleled audio experiences.''',
                "Keyboard": '''Elevate your typing experience with our ergonomic Keyboard. 
                Designed for precision and comfort, it offers customizable backlighting and responsive keys, 
                making it ideal for gamers and typists alike. ''',
                "Mouse": '''Navigate with precision using our high-performance Mouse. 
                Engineered for ergonomic comfort and precision accuracy, it's essential for enhancing productivity and gaming enjoyment with every click. ''',
                }

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    embedding = client.embeddings.create(input=[text], model=model).data[0].embedding
    return embedding


def vector_to_binary(vector):
    return np.array(vector, dtype=np.float32).tobytes()

def binary_to_vector(binary):
    return np.frombuffer(binary, dtype=np.float32)

def populate_with_fake_data(db: Session, num_users=5, num_products=5, num_orders=5):
    # Hardcoded users
    users = [
        User(name="Alice Johnson", username="alicej"),
        User(name="Bob Smith", username="bobsmith"),
        User(name="Charlie Brown", username="charlieb"),
        User(name="Diana Prince", username="dianap"),
        User(name="Evan Wright", username="evanw")
    ]
    db.add_all(users)
    db.commit()

    
    print(Product.__dict__.keys())  
    # Hardcoded products
    products = [
        Product(product_name="Laptop", price=799.99, quantity=50, product_description=descriptions["Laptop"],
                image_path="/images/laptop.jpg", 
                description_embedding=vector_to_binary(get_embedding(descriptions["Laptop"]))),
        Product(product_name="Smartphone", price=499.99, quantity=100, product_description=descriptions["Smartphone"],
                 image_path="/images/smartphone.jpg", 
                 description_embedding=vector_to_binary(get_embedding(descriptions["Smartphone"]))),
        Product(product_name="Headphones", price=199.99, quantity=200, product_description=descriptions["Headphones"],
                image_path="/images/headphones.jpg",
                description_embedding=vector_to_binary(get_embedding(descriptions["Headphones"]))),
        Product(product_name="Keyboard", price=99.99, quantity=150, product_description=descriptions["Keyboard"],
                image_path="/images/keyboard.jpg",
                description_embedding=vector_to_binary(get_embedding(descriptions["Keyboard"]))),
        Product(product_name="Mouse", price=49.99, quantity=300, product_description=descriptions["Mouse"],
                 image_path="/images/mouse.jpg",
                 description_embedding=vector_to_binary(get_embedding(descriptions["Mouse"])))
    ]
    db.add_all(products)
    db.commit()

    # Hardcoded orders
    orders = [
        Order(order_time="2022-06-15 12:30:00", quantity=1, product_id=products[0].id,  user_id = users[0].id),
        Order(order_time="2023-01-20 15:45:00", quantity=2, product_id=products[1].id,  user_id = users[1].id),
        Order(order_time="2021-12-10 09:10:00", quantity=1, product_id=products[2].id,  user_id = users[2].id),
        Order(order_time="2023-03-22 18:05:00", quantity=3, product_id=products[3].id,  user_id = users[3].id),
        Order(order_time="2022-11-05 13:55:00", quantity=2, product_id=products[4].id,  user_id = users[4].id)
    ]
    db.add_all(orders)
    db.commit()

# Use this function
with SessionLocal() as db:
    populate_with_fake_data(db)
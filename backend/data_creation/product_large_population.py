import sys
import os
sys.path.append(os.path.abspath('../'))

import os
import ast
from sentence_transformers import SentenceTransformer
from config import kai_db_link, kai_db_name

from pymongo import MongoClient
import numpy as np


def add_products(category_name):
   
    file_path = os.path.join('category_products', f'{category_name}.json')
    with open(file_path, 'r') as file:
        data = file.read()


    # Remove the outer double quotes
    if data.startswith('"') and data.endswith('"'):
        data = data[1:-1]


    # Check if the string starts with "products = ["
    if data.startswith('products = ['):
        # Remove the "products = " part
        data = data[len('products = '):]


    # Ensure the string ends with ')]'
    if not data.endswith(')]'):
        # The list is incomplete; remove the incomplete entry
        last_complete_entry = data[:data.rfind('),')]
        if last_complete_entry:
            data = last_complete_entry + ')]'


    # Replace escaped characters with their intended counterparts
    data = data.replace('\\\"', '\"').replace('\\n', '\n').replace('\\"', '\"')

    # Convert the cleaned string into a Python list
    products_list = ast.literal_eval(data)

    

    product_names_set = set()

    filtered_products_list = []

    for product in products_list:
        if product[0] in product_names_set:
            continue
        else:
            filtered_products_list.append(product)
            product_names_set.add(product[0])

    print(f"len filtered list: {len(filtered_products_list)}")
    


    model = SentenceTransformer('Alibaba-NLP/gte-large-en-v1.5', trust_remote_code=True)

    descriptions = []
    for product in filtered_products_list:
        descriptions.append(product[3])

    embeddings = model.encode(descriptions)
    normalized_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    db_client = MongoClient(kai_db_link)
    db = db_client[kai_db_name]
    product_collection = db['products']
    
    product_docs = []
    for i in range(len(filtered_products_list)):
        product = filtered_products_list[i]
        product_doc = {
            "product_name": product[0],
            "price": product[1],
            "quantity": product[2],
            "product_description": product[3],
            "image_path": f'/images/category_products/{category_name}.jpeg',
            "description_embedding": normalized_embeddings[i].tolist()
        }
        product_docs.append(product_doc)
    product_ids = product_collection.insert_many(product_docs).inserted_ids
   

directory_path = "category_products"
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    category_name= filename[:-5] 

    print(f"Starting to add {category_name}")
    add_products(category_name)
    print(f"{category_name} added")

    print("")
        
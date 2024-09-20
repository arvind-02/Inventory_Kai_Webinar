from faker import Faker
import random
from config import kai_db_link, kai_db_name
from pymongo import MongoClient
from tqdm import tqdm


# Initialize Faker

fake = Faker()

def generate_username(name):
    parts = name.lower().split()
    if len(parts) > 1:
        return parts[0] + random.choice([parts[-1][0], ''])
    else:
        return parts[0][:6]
    
def generate_users(num_users):
    users = []
    for _ in tqdm(range(num_users)):
        name = fake.name()
        username = generate_username(name)
        users.append({"name": name, "username": username})
    return users



num_users = 3000000
users = generate_users(num_users)
print("Users Generated")


db_client = MongoClient(kai_db_link)
db = db_client[kai_db_name]
user_collection = db['users']
user_ids = user_collection.insert_many(users).inserted_ids
db_client.close()
print("Kai Ingest Done")
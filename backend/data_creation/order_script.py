import sys
import os
sys.path.append(os.path.abspath('../'))
from config import kai_db_link, kai_db_name
from pymongo import MongoClient
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
from tqdm import tqdm

db_client = MongoClient(kai_db_link)
db = db_client[kai_db_name]
product_collection = db['products']
users_collection = db['users']
order_collection = db["orders"] 


product_id_list = [doc['_id'] for doc in product_collection.find({}, {'_id': 1})]
print(f"{len(product_id_list)} products")

users_id_list = [doc['_id'] for doc in users_collection.find({}, {'_id': 1})]
print(f"{len(users_id_list)} users")


orders = []
#Take the number of total orders you want added to your script and divide by 3. Set num_orders to that value
num_orders = 3000000
now = datetime.now()
options = ["long", "year", "year", "year", "month", "month"]
one_month_ago = now - timedelta(days=30)
one_year_ago = now - relativedelta(years=1)
five_years_ago = now - relativedelta(years=5)
for i in tqdm(range(num_orders)):
    random_user_id = random.choice(users_id_list)
    num_user_orders = random.randint(1,5)
    for j in range(num_user_orders):
        options = ["long", "year", "year", "year", "month", "month"]
        option = random.choice(options)
        random_product_id = random.choice(product_id_list)
        
        if option == "year":
            time_between_dates = now - one_year_ago
            seconds_between_dates = time_between_dates.total_seconds()
            random_number_of_seconds = random.randrange(int(seconds_between_dates))
            
            wanted_date =  one_year_ago + timedelta(seconds=random_number_of_seconds)
        
        elif option == "month":
            time_between_dates = now - one_month_ago
            seconds_between_dates = time_between_dates.total_seconds()
            random_number_of_seconds = random.randrange(seconds_between_dates)
            wanted_date = one_month_ago + timedelta(seconds=random_number_of_seconds)
        
        else: 
            time_between_dates = one_year_ago - five_years_ago
            days_between_dates = time_between_dates.days
            random_number_of_days = random.randint(0, days_between_dates)
            
            random_date = five_years_ago + timedelta(days=random_number_of_days)
            
            # Add random time
            random_time = timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )

            wanted_date =random_date + random_time
        
        gen_quantity = random.randint(1, 3)
        orders.append({"order_time": wanted_date, "quantity": gen_quantity, "product_id": random_product_id, "user_id": random_user_id})
        
order_ids = order_collection.insert_many(orders)
print("kai orders inserted")





db_client.close()


    
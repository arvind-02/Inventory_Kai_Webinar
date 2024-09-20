from config import openai_key
from openai import OpenAI
import os 
import json
from tqdm import tqdm

GPT4o_mini = 'gpt-4o-mini'

categories = [
    "Smartphones", "Laptops", "Tablets", "Smartwatches", "Gaming Consoles", 
    "Televisions", "Cameras", "Home Security Systems", "Bluetooth Speakers", 
    "Headphones", "Portable Chargers", "Smart Home Devices", "Fitness Trackers", 
    "Electric Scooters", "Drones", "Robot Vacuums", "Smart Lighting", 
    "Wireless Earbuds", "E-Readers", "3D Printers", "Bicycles", "Motorcycles", 
    "Electric Cars", "Camping Gear", "Hiking Equipment", "Fitness Equipment", 
    "Yoga Accessories", "Running Shoes", "Cycling Gear", "Fishing Gear", 
    "Hunting Equipment", "Golf Equipment", "Tennis Gear", "Skiing Gear", 
    "Surfing Equipment", "Photography Equipment", "Musical Instruments", 
    "DJ Equipment", "Audio Recording Gear", "Home Gym Equipment", "Pet Supplies", 
    "Gardening Tools", "Outdoor Furniture", "Barbecue Grills", "Kitchen Appliances", 
    "Cookware", "Baking Supplies", "Wine Accessories", "Coffee & Tea Equipment", 
    "Baby Products", "Toys & Games", "Board Games", "Puzzles", "Video Games", 
    "Books", "Stationery", "Office Supplies", "Art Supplies", "Craft Supplies", 
    "Sewing Equipment", "Knitting & Crochet Supplies", "Fabric & Textiles", 
    "Costumes & Party Supplies", "Bedding & Linens", "Home Decor", "Lighting Fixtures", 
    "Bathroom Accessories", "Cleaning Supplies", "Storage Solutions", 
    "Luggage & Travel Accessories", "Watches", "Jewelry", "Handbags & Purses", 
    "Footwear", "Men’s Apparel", "Women’s Apparel", "Kids’ Apparel", "Outerwear", 
    "Swimwear", "Sunglasses", "Fragrances", "Skincare Products", "Hair Care Products", 
    "Makeup", "Men’s Grooming", "Health Supplements", "Vitamins", "Protein Powders", 
    "Herbal Remedies", "First Aid Supplies", "Medical Devices", "Dental Care", 
    "Eyewear", "Hearing Aids", "Massage Equipment", "Orthopedic Supplies", 
    "Personal Safety Equipment", "Survival Gear", "Emergency Preparedness", 
    "Fire Safety Equipment"
]


client = OpenAI(
            api_key = openai_key
        )

def make_call(category):
    response = client.chat.completions.create(
          model= GPT4o_mini,
          messages=[
                {"role": "system", "content": "You are Question Answering Portal"},
                {"role": "user", "content": f'''You are an expert at generating data.
                 ''I have an inventory recommendation app, and I'm trying to generate products to populate my database with.
                 I want to generate 100 different products from the category '{category}'. Each product should have a name, a price, a quantity, and a description.
                 Please output a list of products, where each tuple represents the product. The elements of the tuple should be in the order name, price, quantity, description.
                 Make the descriptions around 2 sentences, try to stick to this. Here is an example of the format for two products:

                 Please output a list of 100 products from the category '{category}'. Make it a list of diverse products, don't repeat anything. 
                 Only output the list, nothing else.
                 Don't output "Here is the list of 100 products from the category '{category}'" or anything like that at the start. Also don't output ```python at the start. 
                 Just give me the list of products ready to go into a program. 
                 Also, don't give me more than 100 products. Here is an example output with two products, yours should have 100:

                 [("Laptop", 799.99, 50, "A high-performance laptop suitable for all your computing needs. It features a sleek design and powerful hardware, making it perfect for both work and entertainment." ),("Tablet", 399.99, 60, "A versatile tablet with a vibrant display and long battery life. Ideal for browsing, reading, and on-the-go productivity.")]
                 Again, make sure you dont give me more than 100 product, know when to stop.'''}
            ],
          temperature=0.5
        )

    return response.choices[0].message.content  


folder_name = "category_products"
os.makedirs(folder_name, exist_ok=True)

for category in tqdm(categories):
    category_output = make_call(category)
    file_name = f"{category}.json"

    file_path = os.path.join(folder_name, file_name)
    with open(file_path, "w") as json_file:
        json.dump(category_output, json_file)
    print(f"{category} category done")



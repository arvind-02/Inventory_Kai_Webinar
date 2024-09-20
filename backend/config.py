import os
from dotenv import load_dotenv

load_dotenv(override=True)

db_link = os.getenv("KAI_LINK")
db_name = os.getenv("KAI_DATABASE")
kai_db_link = os.getenv("KAI_LINK")
kai_db_name = os.getenv("KAI_DATABASE")
mongo_db_link = os.getenv("MONGO_LINK")
mongo_db_name = os.getenv("MONGO_DATABASE")
openai_key = os.getenv("OPENAI_API_KEY")
replicate_key = os.getenv("REPLICATE_API_KEY")
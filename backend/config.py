import os
from dotenv import load_dotenv

load_dotenv()

db_link = os.getenv("KAI_LINK")
db_name = os.getenv("KAI_DATABASE")
openai_key = os.getenv("OPENAI_API_KEY")
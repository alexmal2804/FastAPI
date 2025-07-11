import os
from dotenv import load_dotenv
from supabase import Client, create_client
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

mongo_db_url = "mongodb://localhost:27017"
mongo_db_name = "mydatabase"


async def get_supabase():
    supabase = create_client(supabase_url, supabase_key)
    try:
        yield supabase
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        raise e

async def get_mongo_db():
    client = AsyncIOMotorClient(mongo_db_url)
    db = client[mongo_db_name]
    try:
        yield db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise e


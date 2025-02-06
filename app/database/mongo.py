import motor.motor_asyncio
import os
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from dotenv import load_dotenv


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]
fs = AsyncIOMotorGridFSBucket(db)


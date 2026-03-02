from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongodb():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    return db


async def close_mongodb_connection():
    global client
    if client:
        client.close()


def get_database():
    if db is None:
        raise Exception("Database not connected. Call connect_to_mongodb first.")
    return db

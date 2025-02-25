import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME: str = "news_db"

client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
db: AsyncIOMotorDatabase = client[DATABASE_NAME]


async def get_db() -> AsyncIOMotorDatabase:
    """Returns the MongoDB database instance."""
    return db

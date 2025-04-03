import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from lna_db.models.news import AggregatedStory, Article, Source, User

MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME: str = "news_db"

client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
db: AsyncIOMotorDatabase = client[DATABASE_NAME]


async def init_database() -> None:
    """Initialize Beanie with all models. Should be called once during
    application startup."""
    models = [
        User,
        Source,
        Article,
        AggregatedStory,
    ]
    await init_beanie(
        database=db,
        document_models=models,
    )

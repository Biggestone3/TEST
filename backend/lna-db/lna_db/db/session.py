from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorDatabase

from lna_db.db.mongo import get_db as get_real_db
from lna_db.models.news import AggregatedStory, Article, Source, User


async def init_database() -> None:
    """Initialize Beanie with all models. Should be called once during
    application startup."""
    db = await get_real_db()
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


async def get_database() -> AsyncIOMotorDatabase:
    """Returns the database instance. Beanie should already be initialized."""
    return await get_real_db()

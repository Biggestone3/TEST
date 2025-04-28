from typing import TYPE_CHECKING

from beanie import init_beanie

from lna_db.db.db import (
    initialize,  # Import your initialize function  # Import your initialize function
)
from lna_db.models.news import AggregatedStory, Article, Source, User, UserPreferences

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorDatabase

DATABASE_NAME: str = "my_db"


async def init_database(
    username: str,
    password: str,
    mongo_uri_part2: str,
) -> None:
    """Initialize Beanie with all models using the real database."""
    async_client = initialize(
        username=username,
        password=password,
        mongo_uri_part2=mongo_uri_part2,
    )
    db: AsyncIOMotorDatabase = async_client[DATABASE_NAME]

    models = [User, Source, Article, AggregatedStory, UserPreferences]

    await init_beanie(
        database=db,
        document_models=models,
    )

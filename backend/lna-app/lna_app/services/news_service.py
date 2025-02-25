from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase

from lna_app.schema.schema import AggregatedStory


async def fetch_stories(
    db: AsyncIOMotorDatabase,
) -> list[AggregatedStory]:
    """Fetch all stories from MongoDB (supports both async and mock DB)."""

    cursor = db.stories.find()
    raw_stories: list[dict[str, Any]] = [story async for story in cursor]

    return 1
    return [AggregatedStory(**story) for story in raw_stories]

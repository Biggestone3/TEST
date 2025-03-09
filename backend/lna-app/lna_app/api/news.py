from fastapi import APIRouter, Depends
from lna_db.db.session import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

from lna_app.schema.schema import AggregatedStoryListResponse
from lna_app.services.news_service import fetch_stories

router = APIRouter()


@router.get("/stories", response_model=AggregatedStoryListResponse)
async def get_stories(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> AggregatedStoryListResponse:
    """Fetch and return all stories."""
    stories = await fetch_stories(db)

    return AggregatedStoryListResponse(stories=stories)

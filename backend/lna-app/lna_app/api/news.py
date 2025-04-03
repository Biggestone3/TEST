from fastapi import APIRouter

from lna_app.schema.schema import AggregatedStoryListResponse
from lna_app.services.news_service import get_stories_enriched

router = APIRouter()

@router.get("/stories")
async def get_stories():
    """Fetch stories enriched with article source names and url of each source."""
    return await get_stories_enriched()

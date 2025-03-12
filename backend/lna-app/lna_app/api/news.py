from fastapi import APIRouter

from lna_app.schema.schema import AggregatedStoryListResponse
from lna_app.services.news_service import get_stories_paginated

router = APIRouter()


@router.get("/stories", response_model=AggregatedStoryListResponse)
async def get_stories() -> AggregatedStoryListResponse:
    """Fetch and return all stories."""
    stories = await get_stories_paginated()

    return AggregatedStoryListResponse(stories=stories)

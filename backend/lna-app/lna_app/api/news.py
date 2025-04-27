# news.py

from fastapi import APIRouter, FastAPI

from lna_app.schema.schema import (
    AggregatedStoryCreate,
    ArticleCreate,
    ArticleListResponse,
    EnrichedStoryListResponse,
    SourceCreate,
    SourceListResponse,
    StoryFilterRequest,
    UserCreate,
    UserListResponse,
)
from lna_app.services.news_service import (
    create_aggregated_story,
    create_article,
    create_source,
    create_user,
    get_articles_paginated,
    get_enriched_stories,
    get_sources_paginated,
    get_users_paginated,
)

app = FastAPI()
router = APIRouter()


@router.post("/stories", response_model=EnrichedStoryListResponse)
async def get_stories(filter_req: StoryFilterRequest) -> EnrichedStoryListResponse:
    """
    Fetch enriched stories with optional source name filtering.

    - **start_time:** Return stories published after this timestamp.
    - **offset:** Skip this many filtered stories.
    - **page_size:** Return exactly this many filtered stories (after filtering).
    - **sourceNames:** A list of source names to filter stories.
      If empty, stories are returned without additional filtering.
    """
    result = await get_enriched_stories(
        cutoff_date=filter_req.cuttof_date,
        offset=filter_req.offset,
        page_size=filter_req.page_size,
        source_ids=filter_req.source_ids,
    )
    return EnrichedStoryListResponse(enriched_stories=result)


@router.get("/users", response_model=UserListResponse)
async def get_users() -> UserListResponse:
    """Fetch and return all users."""
    users = await get_users_paginated()
    return UserListResponse(users=users)


@router.get("/sources", response_model=SourceListResponse)
async def get_sources() -> SourceListResponse:
    """Fetch and return all sources."""
    sources = await get_sources_paginated()
    return SourceListResponse(sources=sources)


@router.get("/articles", response_model=ArticleListResponse)
async def get_articles() -> ArticleListResponse:
    """Fetch and return all articles."""
    articles = await get_articles_paginated()
    return ArticleListResponse(articles=articles)


@router.post("/sources")
async def create_source_endpoint(source_data: SourceCreate) -> None:
    """Create a new source."""
    await create_source(source_data)


@router.post("/users")
async def create_user_endpoint(user_data: UserCreate) -> None:
    """Create a new user."""
    await create_user(user_data)


@router.post("/articles")
async def create_article_endpoint(article_data: ArticleCreate) -> None:
    """Create a new article."""
    await create_article(article_data)


@router.post("/stories/create")
async def create_story_endpoint(story_data: AggregatedStoryCreate) -> None:
    """Create a new aggregated story."""
    await create_aggregated_story(story_data)


app.include_router(router)

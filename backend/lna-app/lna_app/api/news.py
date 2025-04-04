from fastapi import APIRouter, FastAPI

from lna_app.schema.schema import (
    AggregatedStoryCreate,
    AggregatedStoryListResponse,
    ArticleCreate,
    ArticleListResponse,
    SourceCreate,
    SourceListResponse,
    UserCreate,
    UserListResponse,
)
from lna_app.services.news_service import (
    create_aggregated_story,
    create_article,
    create_source,
    create_user,
    get_articles_paginated,
    get_sources_paginated,
    get_stories_paginated,
    get_users_paginated,
)

app = FastAPI()
router = APIRouter()


@router.get("/stories", response_model=AggregatedStoryListResponse)
async def get_stories() -> AggregatedStoryListResponse:
    """Fetch and return all stories."""
    stories = await get_stories_paginated()
    return AggregatedStoryListResponse(stories=stories)


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


@router.post("/stories")
async def create_story_endpoint(story_data: AggregatedStoryCreate) -> None:
    """Create a new aggregated story."""
    await create_aggregated_story(story_data)


app.include_router(router)

from lna_db.models.news import (
    Article as DbArticle,
)
from fastapi import APIRouter, FastAPI
from lna_app.schema.schema import (
    AggregatedStoryListResponse,
    UserListResponse,
    SourceListResponse,
    ArticleListResponse,
    ArticleCreate,
    UserCreate,
    AggregatedStoryCreate,
    SourceCreate,
)
from lna_app.services.news_service import (
    get_stories_paginated,
    get_users_paginated,
    get_sources_paginated,
    get_articles_paginated,
    create_aggregated_story,
    create_article,
    create_user,
    create_source,
    get_stories_enriched,
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
async def create_source_endpoint(source_data: SourceCreate):
    """Create a new source."""
    new_source = await create_source(source_data)
    return True

@router.post("/users")
async def create_user_endpoint(user_data: UserCreate):
    """Create a new user."""
    new_user = await create_user(user_data)
    return True

@router.post("/articles")
async def create_article_endpoint(article_data: ArticleCreate):
    """Create a new article."""
    new_article = await create_article(article_data)
    return True

@router.post("/stories")
async def create_story_endpoint(story_data: AggregatedStoryCreate):
    """Create a new aggregated story."""
    new_story = await create_aggregated_story(story_data)
    return True

@router.get("/stories_testing")
async def get_stories():
    """Fetch stories enriched with article source names and url of each source."""
    return await get_stories_enriched()
app.include_router(router)


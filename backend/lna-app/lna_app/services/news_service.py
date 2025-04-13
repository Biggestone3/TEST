from typing import Any

from lna_db.core.types import Language
from lna_db.models.news import (
    AggregatedStory as DbAggregatedStory,
)
from lna_db.models.news import (
    Article as DbArticle,
)
from lna_db.models.news import (
    Source as DbSource,
)
from lna_db.models.news import (
    User as DbUser,
)
from lna_db.models.news import (
    UserPreferences,
)

from lna_app.schema.schema import (
    AggregatedStory,
    AggregatedStoryCreate,
    Article,
    ArticleCreate,
    Source,
    SourceCreate,
    User,
    UserCreate,
)


async def get_stories_paginated(
    skip: int = 0, limit: int = 10
) -> list[AggregatedStory]:
    db_stories = await DbAggregatedStory.find().skip(skip).limit(limit).to_list()
    return [AggregatedStory(**story.model_dump()) for story in db_stories]


async def get_users_paginated(skip: int = 0, limit: int = 10) -> list[User]:
    db_users = await DbUser.find().skip(skip).limit(limit).to_list()
    return [User(**user.model_dump()) for user in db_users]


async def get_sources_paginated(skip: int = 0, limit: int = 10) -> list[Source]:
    db_sources = await DbSource.find().skip(skip).limit(limit).to_list()
    return [Source(**source.model_dump()) for source in db_sources]


async def get_articles_paginated(skip: int = 0, limit: int = 10) -> list[Article]:
    db_articles = await DbArticle.find().skip(skip).limit(limit).to_list()
    return [Article(**article.model_dump()) for article in db_articles]


async def create_user(user_data: UserCreate) -> None:
    preference = UserPreferences(**user_data.preferences)
    db_user = DbUser(
        google_id=user_data.google_id,
        uuid=user_data.uuid,
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        preferences=preference,
    )
    await db_user.insert()


async def create_source(source_data: SourceCreate) -> None:
    db_source = DbSource(
        uuid=source_data.uuid,
        url=source_data.url,
        name=source_data.name,
    )
    await db_source.insert()


async def create_article(article_data: ArticleCreate) -> None:
    try:
        # Convert the language field to the Language enum type
        language = Language(article_data.language)
        article = DbArticle(
            uuid=article_data.uuid,
            source_id=article_data.source_id,
            url=article_data.url,
            publish_date=article_data.publish_date,
            title=article_data.title,
            content=article_data.content,
            language=language,
        )
        # Insert the article into the database
        await article.insert()

    except Exception as e:
        # Handle any errors during article creation
        raise ValueError(f"Failed to create article: {str(e)}")


async def create_aggregated_story(story_data: AggregatedStoryCreate) -> None:
    language = Language(story_data.language)
    db_story = DbAggregatedStory(
        uuid=story_data.uuid,
        title=story_data.title,
        summary=story_data.summary,
        language=language,
        publish_date=story_data.publish_date,
        article_ids=story_data.article_ids,
    )
    await db_story.insert()


async def get_stories_enriched() -> list[dict[str, Any]]:
    db_stories = await DbAggregatedStory.find_all().to_list()
    enriched_stories: list[dict[str, Any]] = []

    for story in db_stories:
        # Convert to UUIDs just in case they're strings
        article_ids = [str(aid) for aid in story.article_ids]
        articles = await DbArticle.find({"uuid": {"$in": article_ids}}).to_list()

        source_ids = [str(article.source_id) for article in articles]
        sources = await DbSource.find({"uuid": {"$in": source_ids}}).to_list()
        source_map = {
            str(source.uuid): {"name": source.name, "url": source.url}
            for source in sources
        }
        enriched_articles = [
            {
                "id": str(article.uuid),
                "source_name": source_map.get(str(article.source_id), {}).get(
                    "name", "Unknown Source"
                ),
                "source_url": source_map.get(str(article.source_id), {}).get(
                    "url", None
                ),
            }
            for article in articles
        ]

        enriched_stories.append(
            {
                "id": str(story.id),
                "title": story.title,
                "summary": story.summary,
                "language": story.language.value,
                "publish_date": story.publish_date.isoformat(),
                "articles": enriched_articles,
            }
        )

    return enriched_stories

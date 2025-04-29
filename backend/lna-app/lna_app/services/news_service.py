# services/news_service.py
from datetime import datetime
from typing import Any, Optional

from beanie.operators import And


from beanie import SortDirection
from lna_db.core.types import Language, UUIDstr
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

from lna_app.latency_utils import timeit
from lna_app.schema.schema import (
    AggregatedStory,
    AggregatedStoryCreate,
    Article,
    ArticleCreate,
    EnrichedArticle,
    EnrichedStory,
    Source,
    SourceCreate,
    User,
    UserCreate,
    TimeBasedClusteringRequest,
)

from lna_app.services.clustering import generate_summary
from datetime import datetime, timedelta, timezone
from fastapi import Query

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
        language = Language(article_data.language)
        article = DbArticle(
            uuid=article_data.uuid,
            source_id=article_data.source_id,
            url=article_data.url,
            publish_date=article_data.publish_date,
            title=article_data.title,
            content=article_data.content,
            language=language,
            crawler=article_data.crawler,
        )
        await article.insert()
    except Exception as e:
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
        aggregation_key="",
        aggregator=story_data.aggregator,
    )
    await db_story.insert()


@timeit
async def get_enriched_stories(
    cutoff_date: datetime,
    offset: int = 0,
    page_size: int = 10,
    source_ids: Optional[list[UUIDstr]] = None,
) -> list[EnrichedStory]:
    """
    returns paginated stories sorted by most recent with:
      1. story.publish_date < cutoff_date
      2. if source_ids is provided, story.article_ids must contain at least one article
         whose Article.source_id is in source_ids
    """

    query: dict[str, Any] = {"publish_date": {"$lt": cutoff_date}}
    if source_ids:  # only add the $all clause when list is non‐empty
        query["source_ids"] = {"$all": source_ids}

    matching_stories = (
        await DbAggregatedStory.find(query)
        .sort(
            [
                ("publish_date", SortDirection.DESCENDING),
                ("_id", SortDirection.DESCENDING),
            ]
        )
        .skip(offset)
        .limit(page_size)
        .to_list()
    )

    print(f"matching_stories_count: {len(matching_stories)}")

    # get all matching articles
    matching_article_ids: list[UUIDstr] = []
    for story in matching_stories:
        matching_article_ids.extend([id for id in story.article_ids])
    matching_article_ids = list(set(matching_article_ids))
    matching_articles = await DbArticle.find(
        {"uuid": {"$in": matching_article_ids}}
    ).to_list()
    article_id_to_article: dict[UUIDstr, DbArticle] = {
        article.uuid: article for article in matching_articles
    }

    print(f"matching_articles_count: {len(matching_article_ids)}")

    # get all matching sources
    matching_source_ids = []
    for story in matching_stories:
        matching_source_ids.extend([id for id in story.source_ids])
    matching_source_ids = list(set(matching_source_ids))
    matching_sources = await DbSource.find(
        {"uuid": {"$in": matching_source_ids}}
    ).to_list()
    source_id_to_source: dict[UUIDstr, Source] = {
        article.uuid: Source(uuid=article.uuid, name=article.name, url=article.url)
        for article in matching_sources
    }

    print(f"matching_sources_count: {len(matching_source_ids)}")

    # enrich the stories
    enriched_stories: list[EnrichedStory] = []
    for story in matching_stories:
        articles = [article_id_to_article[uuid] for uuid in story.article_ids]
        enriched_articles = []
        for article in articles:
            if article.source_id in source_id_to_source:
                # only inlcude articles with sources in the story sources.
                enriched_articles.append(
                    EnrichedArticle(
                        id=article.uuid,
                        url=article.url,
                        source_name=source_id_to_source[article.source_id].name,
                        source_url=source_id_to_source[article.source_id].url,
                    )
                )
        enriched_stories.append(
            EnrichedStory(
                id=story.uuid,
                title=story.title,
                summary=story.summary,
                language=story.language,
                publish_date=story.publish_date,
                articles=enriched_articles,
            )
        )

    return enriched_stories

async def cluster_articles_into_stories_by_date(
        time_based_clustering_request: TimeBasedClusteringRequest
) -> None:
    range_begin = time_based_clustering_request.start_time.astimezone(timezone.utc)
    end_time = time_based_clustering_request.end_time.astimezone(timezone.utc)
    if range_begin >= end_time:
        raise ValueError(f"Invalid time range provided. {range_begin=} >= {end_time=}") 
    if range_begin > datetime.now(timezone.utc):
        raise ValueError(f"Invalid time range provided. {range_begin=} > {datetime.now(timezone.utc)=}")
    duration = int(time_based_clustering_request.duration)
    while range_begin < end_time:
        range_end = min(range_begin + timedelta(hours=duration), end_time)

        # Query articles within the specified time range
        db_articles = await DbArticle.find(
            And(
                DbArticle.publish_date > range_begin,
                DbArticle.publish_date < range_end
            )
        ).to_list()

        if not db_articles:
            continue

        summary_generated = generate_summary(db_articles)
        ids = [article.uuid for article in db_articles]

        story = AggregatedStoryCreate(
            uuid=db_articles[0].uuid,
            title=f"News from {range_begin} to {range_end}",
            summary=summary_generated,
            language=db_articles[0].language,
            publish_date=datetime.now(),
            article_ids=ids,
            aggregator="Api_time_based_aggregator",
            aggregation_key=f"News from {range_begin.isoformat()}, to {range_end.isoformat()}",
        )
        range_begin += timedelta(hours=duration)
        await create_aggregated_story(story)
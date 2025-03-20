from lna_db.core.types import Language, UUIDstr
from bson import ObjectId
from lna_db.models.news import (
    AggregatedStory as DbAggregatedStory,
    Article as DbArticle,
    Source as DbSource,
    User as DbUser,
    UserPreferences,
)
from lna_app.schema.schema import (
    AggregatedStory,
    Article,
    Source,
    User,
    ArticleCreate,
    UserCreate,
    SourceCreate,
    AggregatedStoryCreate,
)
from uuid import uuid4
async def get_stories_paginated(skip: int = 0, limit: int = 10) -> list[AggregatedStory]:
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

async def create_user(user_data: UserCreate):
    preference = UserPreferences(**user_data.preferences)
    db_user = DbUser(
        id = ObjectId(),
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        preferences=preference
    )
    await db_user.insert()
    return True

async def create_source(source_data: SourceCreate):
    db_source = DbSource(
        id = ObjectId(),
        url=source_data.url,
        name=source_data.name
    )
    await db_source.insert()
    return True


async def create_article(article_data: ArticleCreate):
    try:
        # Convert the language field to the Language enum type
        language = Language(article_data.language)
        article = DbArticle(
            id = ObjectId(),
            source_id=article_data.source_id,  
            url=article_data.url,                    
            publish_date=article_data.publish_date,  
            title=article_data.title,                
            content=article_data.content,            
            language=language
        )
        # Insert the article into the database
        await article.insert()
        return True

    except Exception as e:
        # Handle any errors during article creation
        raise ValueError(f"Failed to create article: {str(e)}")
async def create_aggregated_story(story_data: AggregatedStoryCreate):
    db_story = DbAggregatedStory(
        id = ObjectId(),
        title = story_data.title, 
        summary = story_data.summary,
        language = story_data.language,
        publish_date = story_data.publish_date,
        article_ids = story_data.article_ids
    )
    await db_story.insert()
    return True
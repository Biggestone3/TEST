# TYPES ===
"""Core types and enums used across the application."""

from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import PlainSerializer


class Language(str, Enum):
    """Language options for content."""

    ENGLISH = "en"
    ARABIC = "ar"
    UNKNOWN = "unknown"


# Custom type that maintains UUID type safety internally but serializes to string
# in API responses. This ensures consistent UUID handling across the application
# while providing clean string-based UUIDs in JSON responses and MongoDB storage.
UUIDstr = Annotated[UUID, PlainSerializer(lambda x: str(x), return_type=str)]


# === MODELS ===
from datetime import UTC, datetime
from typing import Annotated, Any, Self
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field



class TimeStampedModel(Document):
    """Base model with created and updated timestamps."""

    id: UUID = Field(default_factory=uuid4)  # pyre-ignore
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the model was created",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Timestamp when the model was last updated",
    )

    class Settings:
        use_state_management = True

    async def save(self, *args: Any, **kwargs: Any) -> Self:
        self.updated_at = datetime.now(UTC)
        return await super().save(*args, **kwargs)


class UserPreferences(Document):
    """User preferences model."""

    source_ids: list[UUIDstr] = Field(
        default_factory=list, description="List of Source IDs that the user follows."
    )
    language: Language = Field(
        default=Language.UNKNOWN, description="Preferred language for reading news."
    )


class User(TimeStampedModel):
    """User model for the application."""

    email: Annotated[EmailStr, Indexed(unique=True)] = Field(
        ..., description="Email address of the user"
    )
    username: Annotated[str, Indexed(unique=True)] = Field(
        ..., description="Username of the user"
    )
    full_name: str = Field(..., description="Full name of the user")
    preferences: UserPreferences = Field(default_factory=lambda: UserPreferences())

    class Settings:
        name = "users"


class Source(TimeStampedModel):
    """News source model."""

    name: str = Field(..., description="Display name of the source")
    url: str = Field(..., description="URL associated with this source")
    content_html_key: tuple[str, str] = Field(
        default=("", ""), description="The place to get info from the actual webpage."
    )
    has_rss: bool = Field(
        default=True,
        description="Boolean value that determines whether "
        "a webpage has an RSS value or not.",
    )

    class Settings:
        name = "sources"


class Article(TimeStampedModel):
    """Article model representing a news article."""

    source_id: UUIDstr = Field(
        ..., description="Reference to the Source this article belongs to"
    )
    url: Annotated[str, Indexed(unique=True)] = Field(
        ..., description="URL of the article"
    )
    publish_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Publish date of the article",
    )
    title: str = Field(..., description="Title of the article")
    content: str = Field(..., description="Content of the article")
    summary: str = Field(default="", description="Summary of the article")
    language: Language = Language.UNKNOWN

    class Settings:
        name = "articles"


class AggregatedStory(TimeStampedModel):
    """Model representing a clustered or aggregated news story."""

    title: str = Field(..., description="Title of the aggregated story")
    summary: str = Field(..., description="Summary of the aggregated story")
    language: Language = Field(..., description="Language of the aggregated story")
    publish_date: datetime = Field(
        ..., description="Publish date of the aggregated story"
    )
    article_ids: list[UUIDstr] = Field(default_factory=list)

    class Settings:
        name = "stories"


# === CRAWLER LOGIC ===
# Standard Library Imports
import asyncio
import logging
import uuid
from datetime import datetime

import azure.functions as func
import beanie
import feedparser

# Third-Party Library Imports
import httpx
import mongomock_motor
from bs4 import BeautifulSoup
from dateutil import parser
from langdetect import detect

article_Dict = {}


async def fetch_content(
    link: str, myArticle: Article, source_articles: list[Article], src: Source  # noqa: F821 # type: ignore
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(link, timeout=10, follow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        article_content = soup.find(
            src.content_html_key[0], class_=src.content_html_key[1]
        )
        if myArticle.title and len(myArticle.title) > 3:
            try:
                lang_code = detect(myArticle.title)
                # Use unknown as default if failed detection
                myArticle.language = (
                    Language(lang_code)# noqa: F821 # type: ignore
                    if lang_code in Language.__members__.values()# noqa: F821 # type: ignore
                    else Language.UNKNOWN# noqa: F821 # type: ignore
                )
            except Exception:
                myArticle.language = Language.UNKNOWN  # type: ignore # noqa: F821
        if not article_content:
            myArticle.content = "No content to be displayed."
            source_articles.append(myArticle)
            return

        article_content = article_content.get_text(strip=True, separator="\n")
        if len(article_content) < 1:
            myArticle.content = "No content to be displayed."
        else:
            myArticle.content = article_content
        source_articles.append(myArticle)

    except Exception as e:
        print(f"Error in fetch_content ({src.name}): {e}")


async def process_feed_entry(entry, source_articles: list[Article], src: Source):# type: ignore # noqa: F821
    try:
        id = uuid.uuid4()
        myArticle = Article(# type: ignore # noqa: F821
            id=id,
            source_id=src.id,
            content="No content to be displayed.",
            title=entry.title,
            url=entry.link,
            publish_date=datetime.min,
        )
        myArticle.publish_date = parser.parse(entry.published)
        await fetch_content(entry.link, myArticle, source_articles, src)
    except Exception as e:
        print(f"Error in process_feed_entry ({src.name}): {e}")


async def get_feed(src: Source, article_count: int):# type: ignore # noqa: F821
    source_articles = []

    if not src.has_rss:
        await fetch_articles(source_articles, src, article_count)
        return

    feed = feedparser.parse(src.url)
    tasks = [
        asyncio.create_task(process_feed_entry(entry, source_articles, src))
        for entry in feed.entries[:article_count]
    ]

    await asyncio.gather(*tasks)
    article_Dict[src.id] = source_articles
    await add_articles_to_db(src, source_articles)


async def add_articles_to_db(src: Source, data_array: list[Article]):# type: ignore # noqa: F821
    for article in data_array:
        existing_article = await Article.find_one({"url": article.url})# type: ignore # noqa: F821
        if existing_article:
            print("skipped")
            continue  # Skip inserting duplicates
        await article.save()


async def fetch_articles(
    source_articles: list[Article], src: Source, article_count: int# type: ignore # noqa: F821
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(src.url, timeout=10)
            response.raise_for_status()
            data = response.json()

        articles = data.get("articles", [])
        tasks = []

        for article in articles[:article_count]:
            id = uuid.uuid4()
            url = article["websiteUrl"]
            myArticle = Article(# type: ignore # noqa: F821
                id=id,
                url=url,
                source_id=src.id,
                content="No content to be displayed.",
                title=article["name"],
                publish_date=parser.parse(article["date"]),
            )
            tasks.append(
                asyncio.create_task(
                    fetch_content(
                        article["websiteUrl"], myArticle, source_articles, src
                    )
                )
            )

        await asyncio.gather(*tasks)
        article_Dict[src.id] = source_articles
        await add_articles_to_db(src, source_articles)

    except Exception as e:
        print(f"Error in fetch_articles: {e}")


async def auto_get_feed(src: Source, article_count: int):# type: ignore # noqa: F821
    while True:
        await get_feed(src, article_count)


async def start(user: User, article_count: int, refresh_timestamp: int, sources: dict):# type: ignore # noqa: F821
    tasks = []
    for srcid in user.preferences.source_ids:
        source = sources.get(str(srcid))
        if source:
            tasks.append(asyncio.create_task(auto_get_feed(source, article_count)))

    await asyncio.gather(*tasks)


async def init_db():
    """Initialize an in-memory MongoDB for testing using mongomock_motor."""

    # Create an async in-memory MongoDB client
    client = mongomock_motor.AsyncMongoMockClient()
    database = client["test_database"]  # Create a mock database

    # Initialize Beanie with the mock database
    await beanie.init_beanie(
        database=database,  # type: ignore
        document_models=[UserPreferences, User, Source, Article, AggregatedStory],# type: ignore # noqa: F821
    )


async def main():
    # Initialize Beanie before using models
    await init_db()
    # Simulate a test user and sources
    sourceArr = {
        (uuid.UUID(int=0)): Source(# type: ignore # noqa: F821
            id=uuid.UUID(int=0),
            name="almanar",
            url="https://almanar.com.lb/rss",
            content_html_key=("div", "article-content"),
            has_rss=True,
        ),
        (uuid.UUID(int=1)): Source(# type: ignore # noqa: F821
            id=uuid.UUID(int=1),
            name="aljadeed",
            url="https://www.aljadeed.tv/Rss/latest-news",
            content_html_key=("div", "LongDesc text-title-9"),
            has_rss=True,
        ),
        (uuid.UUID(int=2)): Source(# type: ignore # noqa: F821
            id=uuid.UUID(int=2),
            name="mtv",
            url="https://vodapi.mtv.com.lb/api/Service/GetArticlesByNewsSectionID?id=1&start=0&end=20&keywordId=-1&onlyWithSource=false&type=&authorId=-1&platform=&isLatin=",
            content_html_key=("p", "_pragraphs"),
            has_rss=False,
        ),
    }

    # Run feed fetching **only once** per source
    tasks = [asyncio.create_task(get_feed(source, 5)) for source in sourceArr.values()]

    await asyncio.gather(*tasks)

    stored_articles = await Article.find_all().to_list()# type: ignore # noqa: F821
    print("\n=== ARTICLES IN DATABASE ===")

    for article in stored_articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Date: {article.publish_date}")
        print(f"Content: {article.content[:100]}\n")  # Print first 100 characters


app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */3 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)  # noqa: E501
def LnaCrawlerTimer(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function started.")
    try:
        result = main()  # change if your Crawler has a different entrypoint
        logging.info(f"Crawler completed: {result}")
    except Exception as e:
        logging.error(f"Error running crawler: {str(e)}")
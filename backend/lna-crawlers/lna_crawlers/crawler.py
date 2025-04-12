# Standard Library Imports
import asyncio
import logging
import os
import uuid
from datetime import datetime

import azure.functions as func
import beanie
import feedparser

# Third-Party Library Imports
import httpx
from bs4 import BeautifulSoup
from dateutil import parser
from langdetect import detect
from lna_db.core.types import Language
from lna_db.models.news import AggregatedStory, Article, Source, User, UserPreferences
from motor.motor_asyncio import AsyncIOMotorClient

article_Dict = {}


async def fetch_content(
    link: str, myArticle: Article, source_articles: list[Article], src: Source
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
                    Language(lang_code)
                    if lang_code in Language.__members__.values()
                    else Language.UNKNOWN
                )
            except Exception:
                myArticle.language = Language.UNKNOWN
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


async def process_feed_entry(entry, source_articles: list[Article], src: Source):
    try:
        id = uuid.uuid4()
        myArticle = Article(
            uuid=id,
            source_id=src.uuid,
            content="No content to be displayed.",
            title=entry.title,
            url=entry.link,
            publish_date=datetime.min,
        )
        dt = parser.parse(entry.published)
        myArticle.publish_date = dt
        await fetch_content(entry.link, myArticle, source_articles, src)
    except Exception as e:
        print(f"Error in process_feed_entry ({src.name}): {e}")


async def get_feed(src: Source, article_count: int):
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


async def add_articles_to_db(src: Source, data_array: list[Article]):
    for article in data_array:
        try:
            existing_article = await Article.find_one({"url": article.url})
            if existing_article:
                print("skipped")
                continue  # Skip inserting duplicates
            await article.save()
        except Exception as e:
            print(f"Error occured in adding to DB: {e}")


async def fetch_articles(
    source_articles: list[Article], src: Source, article_count: int
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
            dt = parser.parse(article["date"])
            myArticle = Article(
                uuid=id,
                url=url,
                source_id=src.uuid,
                content="No content to be displayed.",
                title=article["name"],
                publish_date=dt,
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
        print(f"Error in fetch_articles : {e}")


async def auto_get_feed(src: Source, article_count: int):
    while True:
        await get_feed(src, article_count)


async def start(user: User, article_count: int, sources: dict):
    tasks = []
    for srcid in user.preferences.source_ids:
        source = sources.get(str(srcid))
        if source:
            tasks.append(asyncio.create_task(auto_get_feed(source, article_count)))

    await asyncio.gather(*tasks)


async def init_db():
    #uri of DB set as secret on Azure
    uri = os.environ.get("MONGODB_URI")
    client = AsyncIOMotorClient(uri) # Create an async client for MongoDB Atlas
    database = client["my_db"]

    # Initialize Beanie with the real MongoDB
    await beanie.init_beanie(
        database=database,
        document_models=[UserPreferences, User, Source, Article, AggregatedStory],
    )
async def main():
    # Initialize Beanie before using models
    await init_db()
    # Simulate a test user and sources
    sourceArr = {
        (uuid.UUID(int=0)): Source(
            uuid=uuid.UUID(int=0),
            name="almanar",
            url="https://almanar.com.lb/rss",
            content_html_key=("div", "article-content"),
            has_rss=True,
        ),
        (uuid.UUID(int=1)): Source(
            uuid=uuid.UUID(int=1),
            name="aljadeed",
            url="https://www.aljadeed.tv/Rss/latest-news",
            content_html_key=("div", "LongDesc text-title-9"),
            has_rss=True,
        ),
        (uuid.UUID(int=2)): Source(
            uuid=uuid.UUID(int=2),
            name="mtv",
            url="https://vodapi.mtv.com.lb/api/Service/GetArticlesByNewsSectionID?id=1&start=0&end=20&keywordId=-1&onlyWithSource=false&type=&authorId=-1&platform=&isLatin=",
            content_html_key=("p", "_pragraphs"),
            has_rss=False,
        ),
    }

    # Run feed fetching **only once** per source
    tasks = [asyncio.create_task(get_feed(source, 5)) for source in sourceArr.values()]

    await asyncio.gather(*tasks)



app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 */3 * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def LnaCrawlerTimer(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due")

    logging.info("Python timer trigger function started!")
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"Error: {str(e)}")

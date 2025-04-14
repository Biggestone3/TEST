import datetime
import logging
import os
from datetime import UTC

from dotenv import load_dotenv
from lna_db.core.types import Language
from lna_db.db.mongo import init_database
from lna_db.models.news import AggregatedStory


async def time_based_aggregator():
    # Initialize the database connection
    load_dotenv()
    username = str(os.environ.get("username_of_db"))
    password = str(os.environ.get("password_of_db"))
    mongo_uri_part2 = str(os.environ.get("mongo_uri_part2"))

    await init_database(
        username=username,
        password=password,
        mongo_uri_part2=mongo_uri_part2,
    )

    # Create a new aggregated story
    story = AggregatedStory(
        title="test azure function",
        summary="This is a test story created by the Azure Function",
        language=Language.ENGLISH,
        publish_date=datetime.datetime.now(UTC),
        article_ids=[],
    )

    # Save the story to the database
    saved_story = await story.save()

    logging.info(f"Successfully created story with ID: {saved_story.uuid}")

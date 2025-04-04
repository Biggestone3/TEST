import unittest
from datetime import UTC, datetime

from lna_app.services.news_service import get_stories_paginated
from lna_db.core.types import Language
from lna_db.db.mock_db import init_mock_db
from lna_db.models.news import AggregatedStory


class TestNewsService(unittest.IsolatedAsyncioTestCase):
    """Test the news service layer."""

    async def asyncSetUp(self) -> None:
        """Set up test database before each test."""
        await init_mock_db()
        # await init_database()
        # Clear all stories before each test
        await AggregatedStory.delete_all()

    async def test_fetch_stories_with_data(self) -> None:
        """Test fetching stories when data exists."""
        # Add test data
        test_story = {
            "title": "Test Story",
            "summary": "Test summary",
            "language": Language.ENGLISH,
            "publish_date": datetime.now(UTC),
            "article_ids": [],
        }
        story = AggregatedStory(**test_story)
        await story.save()

        # Fetch stories
        stories = await get_stories_paginated()

        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0].title, test_story["title"])
        self.assertEqual(stories[0].summary, test_story["summary"])
        self.assertEqual(stories[0].language, test_story["language"])

    async def test_fetch_stories_empty(self) -> None:
        """Test fetching stories when no data exists."""
        # Clear all stories
        await AggregatedStory.delete_all()

        # Fetch stories
        stories = await get_stories_paginated()

        self.assertEqual(len(stories), 0)

    async def test_fetch_stories_multiple(self) -> None:
        """Test fetching multiple stories."""
        # Add multiple test stories
        test_stories = [
            {
                "title": f"Test Story {i}",
                "summary": f"Test summary {i}",
                "language": Language.ENGLISH,
                "publish_date": datetime.now(UTC),
                "article_ids": [],
            }
            for i in range(3)
        ]

        for story_data in test_stories:
            story = AggregatedStory(**story_data)
            await story.save()

        # Fetch stories
        stories = await get_stories_paginated()

        self.assertEqual(len(stories), 3)
        self.assertEqual(
            sorted([s.title for s in stories]),
            sorted([s["title"] for s in test_stories]),
        )

import unittest
from datetime import UTC, datetime

from pydantic import ValidationError

from lna_app.core.types import Language
from lna_app.schema.schema import AggregatedStory, AggregatedStoryListResponse


class TestSchema(unittest.TestCase):
    """Test schema validation for news stories."""

    def test_valid_story(self):
        """Test creating a valid AggregatedStory."""
        story_data = {
            "title": "Test Story",
            "summary": "Test summary",
            "language": Language.ENGLISH,
            "publish_date": datetime.now(UTC),
            "article_ids": [],
        }
        story = AggregatedStory(**story_data)
        self.assertEqual(story.title, story_data["title"])
        self.assertEqual(story.summary, story_data["summary"])
        self.assertEqual(story.language, story_data["language"])
        self.assertEqual(story.article_ids, story_data["article_ids"])

    def test_invalid_story_missing_fields(self):
        """Test that validation fails when required fields are missing."""
        invalid_data = {
            "title": "Test Story",
            "summary": "Test summary",
            # Missing required fields
        }
        with self.assertRaises(ValidationError):
            AggregatedStory(**invalid_data)

    def test_invalid_story_wrong_types(self):
        """Test that validation fails with wrong field types."""
        invalid_data = {
            "title": "Test Story",
            "summary": "Test summary",
            "language": "invalid_language",  # Invalid language enum
            "publish_date": "invalid-date",  # Invalid date format
            "article_ids": "not-a-list",  # Invalid list type
        }
        with self.assertRaises(ValidationError):
            AggregatedStory(**invalid_data)

    def test_story_list_response(self):
        """Test creating a valid story list response."""
        story_data = {
            "title": "Test Story",
            "summary": "Test summary",
            "language": Language.ENGLISH,
            "publish_date": datetime.now(UTC),
            "article_ids": [],
        }
        story = AggregatedStory(**story_data)
        response = AggregatedStoryListResponse(stories=[story])
        self.assertEqual(len(response.stories), 1)
        self.assertEqual(response.stories[0].title, story_data["title"])

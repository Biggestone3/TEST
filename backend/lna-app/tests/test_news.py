import unittest

from fastapi.testclient import TestClient
from lna_app.main import app
from lna_db.db.mock_db import init_mock_db
from lna_db.models.news import AggregatedStory


class TestNewsAPI(unittest.IsolatedAsyncioTestCase):
    """Test the FastAPI news API using get_mock_db()."""

    async def asyncSetUp(self) -> None:
        """Override FastAPI's get_database() dependency before each test."""
        # Initialize the mock database
        await init_mock_db()
        self.client = TestClient(app)

    async def asyncTearDown(self) -> None:
        """Reset FastAPI dependencies after each test."""
        app.dependency_overrides.clear()

    def test_get_stories(self) -> None:
        """Test fetching stories from the API using get_mock_db()."""
        response = self.client.get("/news/stories")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("stories", data)
        self.assertIsInstance(data["stories"], list)
        self.assertGreater(len(data["stories"]), 0)

    async def test_get_stories_empty(self) -> None:
        """Test when the database returns no stories."""
        await AggregatedStory.delete_all()
        response = self.client.get("/news/stories")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn("stories", data)
        self.assertEqual(len(data["stories"]), 0)

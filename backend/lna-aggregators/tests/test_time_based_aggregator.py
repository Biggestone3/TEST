import unittest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from lna_aggregators.time_based_aggregator import TimeBasedAggregator


class TestTimeBasedAggregator(unittest.IsolatedAsyncioTestCase):
    """Test the TimeBasedAggregator class."""

    async def asyncSetUp(self) -> None:
        """Set up the test environment before each test."""
        # Mock database initialization
        self.mock_init_db = patch(
            "lna_aggregators.time_based_aggregator.init_database"
        ).start()
        self.mock_init_db.return_value = AsyncMock()

        self.aggregator = TimeBasedAggregator(
            database_username="test_user",
            database_password="test_pass",
            mongo_uri_part2="test_uri",
        )

    async def asyncTearDown(self) -> None:
        """Clean up after each test."""
        patch.stopall()

    def test_get_aggregation_key(self) -> None:
        """Test the _get_aggregation_key method."""
        # Test with a specific time
        test_time = datetime(2024, 3, 15, 14, 30, tzinfo=timezone.utc)
        expected_key = "2024-03-15 14:00:00+00:00_2024-03-15 15:00:00+00:00"
        result = self.aggregator._get_aggregation_key(test_time)
        self.assertEqual(result, expected_key)

        # Test with time at the start of an hour
        test_time = datetime(2024, 3, 15, 14, 0, tzinfo=timezone.utc)
        expected_key = "2024-03-15 14:00:00+00:00_2024-03-15 15:00:00+00:00"
        result = self.aggregator._get_aggregation_key(test_time)
        self.assertEqual(result, expected_key)

    def test_get_aggregation_key_and_next_hour(self) -> None:
        """Test the _get_aggregation_key_and_next_hour method."""
        test_time = datetime(2024, 3, 15, 14, 30, tzinfo=timezone.utc)
        expected_key = "2024-03-15 14:00:00+00:00_2024-03-15 15:00:00+00:00"
        expected_next_hour = datetime(2024, 3, 15, 15, 0, tzinfo=timezone.utc)

        key, next_hour = self.aggregator._get_aggregation_key_and_next_hour(test_time)
        self.assertEqual(key, expected_key)
        self.assertEqual(next_hour, expected_next_hour)

    async def test_aggregate_stories_no_articles(self) -> None:
        """Test aggregating stories when no articles are found."""
        # Create a mock for the publish_date field that supports comparisons
        mock_publish_date = MagicMock()
        mock_publish_date.__ge__ = MagicMock(return_value=True)
        mock_publish_date.__le__ = MagicMock(return_value=True)

        # Mock Article class with the publish_date field
        mock_article = MagicMock()
        mock_article.publish_date = mock_publish_date
        mock_article.find = MagicMock(
            return_value=MagicMock(to_list=AsyncMock(return_value=[]))
        )

        # Mock AggregatedStory class
        mock_story = MagicMock()
        mock_story.find = MagicMock(
            return_value=MagicMock(to_list=AsyncMock(return_value=[]))
        )

        with (
            patch("lna_aggregators.time_based_aggregator.Article", mock_article),
            patch("lna_aggregators.time_based_aggregator.AggregatedStory", mock_story),
        ):
            # Act
            start_time = datetime(2024, 3, 15, 14, 0, tzinfo=timezone.utc)
            end_time = datetime(2024, 3, 15, 15, 0, tzinfo=timezone.utc)
            await self.aggregator.aggregate_stories(start_time, end_time)

            # Assert
            mock_article.find.assert_called_once()
            mock_story.find.assert_called_once()
            self.mock_init_db.assert_called_once()

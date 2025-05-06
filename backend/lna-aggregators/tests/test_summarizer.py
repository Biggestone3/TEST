import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from google.genai.types import GenerateContentResponse
from lna_aggregators.summarizer import Summarizer


class TestSummarizer(unittest.IsolatedAsyncioTestCase):
    """Test the Summarizer class using mocked Gemini client."""

    async def asyncSetUp(self) -> None:
        """Set up the mock Gemini client before each test."""
        self.mock_patcher = patch("lna_aggregators.summarizer.genai.Client")
        self.mock_client = self.mock_patcher.start()

        # Create a mock response
        mock_response = MagicMock(spec=GenerateContentResponse)
        mock_response.text = "This is a test summary"

        # Create a mock model
        mock_model = MagicMock()
        mock_model.generate_content = AsyncMock(return_value=mock_response)

        # Create a mock client
        self.mock_client_instance = MagicMock()
        self.mock_client_instance.models = mock_model
        self.mock_client.return_value = self.mock_client_instance

        self.summarizer = Summarizer(gemeni_client=self.mock_client_instance)

    async def asyncTearDown(self) -> None:
        """Clean up after each test."""
        self.mock_patcher.stop()

    async def test_generate_summary(self) -> None:
        """Test the generate_summary method."""
        # Arrange
        previous_summary = "Previous news summary"
        new_articles_content = "New article content"
        output_language = "arabic"

        # Act
        result = await self.summarizer.generate_summary(
            previous_summary=previous_summary,
            new_articles_content=new_articles_content,
            output_language=output_language,
        )

        # Assert
        self.assertEqual(result, "This is a test summary")
        self.mock_client_instance.models.generate_content.assert_called_once()
        call_args = self.mock_client_instance.models.generate_content.call_args
        self.assertEqual(call_args[1]["model"], "gemini-2.0-flash")
        self.assertIn("arabic", call_args[1]["config"].system_instruction)

    async def test_generate_title(self) -> None:
        """Test the generate_title method."""
        # Arrange
        summary = "Test summary content"
        output_language = "arabic"

        # Act
        result = await self.summarizer.generate_title(
            summary=summary, output_language=output_language
        )

        # Assert
        self.assertEqual(result, "This is a test summary")
        self.mock_client_instance.models.generate_content.assert_called_once()
        call_args = self.mock_client_instance.models.generate_content.call_args
        self.assertEqual(call_args[1]["model"], "gemini-2.0-flash")
        self.assertIn("arabic", call_args[1]["config"].system_instruction)
        self.assertEqual(call_args[1]["config"].max_output_tokens, 40)

    async def test_generate_summary_with_empty_inputs(self) -> None:
        """Test generate_summary with empty inputs."""
        # Act
        result = await self.summarizer.generate_summary(
            previous_summary="", new_articles_content="", output_language="arabic"
        )

        # Assert
        self.assertEqual(result, "This is a test summary")
        self.mock_client_instance.models.generate_content.assert_called_once()

    async def test_generate_title_with_empty_summary(self) -> None:
        """Test generate_title with empty summary."""
        # Act
        result = await self.summarizer.generate_title(
            summary="", output_language="arabic"
        )

        # Assert
        self.assertEqual(result, "This is a test summary")
        self.mock_client_instance.models.generate_content.assert_called_once()

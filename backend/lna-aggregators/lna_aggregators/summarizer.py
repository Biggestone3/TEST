import asyncio
import logging
import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.api_core import exceptions
from google.genai import types
from google.genai.client import AsyncClient


class Summarizer:
    def __init__(self, gemeni_client: AsyncClient | None = None):
        if gemeni_client is None:
            load_dotenv()
            gemeni_key = str(os.environ.get("gemeni_key"))
            gemeni_client = genai.Client(api_key=gemeni_key).aio
        self.gemeni_client: AsyncClient = gemeni_client
        self.max_retries = 5
        self.initial_delay = 2  # seconds
        self.max_delay = 64  # seconds

    async def _make_api_call_with_retry(
        self,
        model: str,
        contents: list[str],
        config: types.GenerateContentConfig,
        operation_name: str,
    ) -> str:
        """Make an API call with exponential backoff retry logic."""
        delay = self.initial_delay
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                response = await self.gemeni_client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config,
                )
                return response.text

            except exceptions.ResourceExhausted as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Get retry delay from error details if available
                    retry_delay = None
                    for detail in e.details:
                        if hasattr(detail, "retry_delay"):
                            retry_delay = int(detail.retry_delay.total_seconds())
                            break

                    # Use provided retry delay or calculate exponential backoff
                    wait_time = (
                        retry_delay if retry_delay else min(delay, self.max_delay)
                    )
                    logging.warning(
                        f"Rate limit hit for {operation_name}. "
                        f"Retrying in {wait_time} seconds (attempt "
                        + f"{attempt + 1}/{self.max_retries})"
                    )
                    await asyncio.sleep(wait_time)
                    delay *= 2  # Exponential backoff
                continue

            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    wait_time = min(delay, self.max_delay)
                    logging.warning(
                        f"Error in {operation_name}. "
                        f"Retrying in {wait_time} seconds (attempt {attempt + 1}"
                        + f"/{self.max_retries}): {str(e)}"
                    )
                    await asyncio.sleep(wait_time)
                    delay *= 2
                continue

        # If we've exhausted all retries, raise the last exception
        raise last_exception or Exception(
            f"Failed to complete {operation_name} after {self.max_retries} attempts"
        )

    async def generate_summary(
        self,
        previous_summary: str,
        new_articles_content: str,
        output_language: str = "arabic",
    ) -> str:
        config = types.GenerateContentConfig(
            system_instruction=f"""
        You are an assistant responsible of aggregating news happening in Lebanon.
        Your task is to generate a summary for what happened during a certain period.
        You will be given the current summary (if any) which was generated from other
        articles corresponding to the same period, and you will be given the content
        of the new articles. Please generate a summary which would describe what
        happened in this period. The summary should capture all the important points.
        You summary needs to be in the following language: {output_language}.
        """,
            max_output_tokens=1000,
            temperature=0.1,
        )

        contents = [
            f"""[current summary]
        {previous_summary}
        [content of new articles]
        {new_articles_content}
                        """
        ]

        response_text = await self._make_api_call_with_retry(
            model="gemini-2.0-flash",
            contents=contents,
            config=config,
            operation_name="generate_summary",
        )

        logging.info(
            f"generated a summary of length {len(response_text)} for previous summary"
            + f" of length {len(previous_summary)} and new article contents of length"
            + f" {len(new_articles_content)}"
        )

        return response_text

    async def generate_title(
        self,
        summary: str,
        output_language: str = "arabic",
    ) -> str:
        config = types.GenerateContentConfig(
            system_instruction=f"""
You are an assistant responsible of aggregating news happening in Lebanon.
You previously generated a summary for the news articles during a certain period.
Your task is to generate a title for those articles.
The title should be descriptive.
The title needs to be in the following language: {output_language}.
""",
            max_output_tokens=40,
            temperature=0.1,
        )

        contents = [f"[Summary]\n{summary}"]

        response_text = await self._make_api_call_with_retry(
            model="gemini-2.0-flash",
            contents=contents,
            config=config,
            operation_name="generate_title",
        )

        logging.info(
            f"generated a title of length {len(response_text)} for summary of"
            + f" length {len(summary)}"
        )
        return response_text

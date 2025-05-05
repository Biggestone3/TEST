import logging
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


class Summarizer:
    def __init__(self, gemeni_client: genai.Client | None = None):
        if gemeni_client is None:
            load_dotenv()
            gemeni_key = str(os.environ.get("gemeni_key"))
            gemeni_client = genai.Client(api_key=gemeni_key)
        self.gemeni_client: genai.Client = gemeni_client

    async def generate_summary(
        self,
        previous_summary: str,
        new_articles_content: str,
        output_language: str = "arabic",
    ) -> str:
        response = self.gemeni_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                f"""[current summary]
        {previous_summary}
        [content of new articles]
        {new_articles_content}
                        """
            ],
            config=types.GenerateContentConfig(
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
            ),
        )

        logging.info(
            f"generated a summary of length {len(response.text)} for previous summary"
            + f" of length {len(previous_summary)} and new article contents of length"
            + f" {len(new_articles_content)}"
        )

        return response.text

    async def generate_title(
        self,
        summary: str,
        output_language: str = "arabic",
    ) -> str:
        response = self.gemeni_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"[Summary]\n{summary}"],
            config=types.GenerateContentConfig(
                system_instruction=f"""
You are an assistant responsible of aggregating news happening in Lebanon.
You previously generated a summary for the news articles during a certain period.
Your task is to generate a title for those articles.
The title should be descriptive.
The title needs to be in the following language: {output_language}.
""",
                max_output_tokens=40,
                temperature=0.1,
            ),
        )
        logging.info(
            f"generated a title of length {len(response.text)} for summary of"
            + f" length {len(summary)}"
        )
        return response.text

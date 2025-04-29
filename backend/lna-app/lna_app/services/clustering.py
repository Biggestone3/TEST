from lna_app.schema.schema import Article
from google import genai
from dotenv import load_dotenv
import os
import tiktoken # poetry add tiktoken
from typing import List

# Approximate token limit for Gemini-2 models
MAX_TOKENS = 30000

def estimate_tokens(text: str) -> int:
    # Rough estimate using tiktoken (more accurate for OpenAI but decent for Gemini too)
    enc = tiktoken.get_encoding("cl100k_base")  # most compatible encoding
    return len(enc.encode(text))

def generate_summary(articles: List[Article]) -> str:
    load_dotenv()
    llm_api_key = str(os.environ.get("GEMINI_KEY"))

    # Initial system prompt
    prompt_intro = (
        "أنت مساعد ذكي. لديك مجموعة من الأخبار التالية، كل واحدة بعنوانها ومحتواها الكامل. "
        "يرجى قراءة جميع الأخبار وتوليد ملخص شامل وموجز لها جميعاً باللغة العربية. "
        "المحتوى:\n\n"
    )
    prompt_token_budget = MAX_TOKENS - estimate_tokens(prompt_intro)

    contents = ""
    for article in articles:
        section = f"Title: {article.title}\nContent: {article.content}\n\n"
        if estimate_tokens(contents + section) > prompt_token_budget:
            break
        contents += section

    client = genai.Client(api_key=llm_api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt_intro + contents
    )
    return response.text

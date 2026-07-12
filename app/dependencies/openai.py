from openai import AsyncOpenAI
from app.core.config import get_settings
from functools import lru_cache


@lru_cache
def get_openai_client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

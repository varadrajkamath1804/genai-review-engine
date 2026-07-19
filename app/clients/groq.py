from groq import AsyncGroq

from app.core.config import get_settings

settings = get_settings()


def create_groq_client() -> AsyncGroq:
    return AsyncGroq(api_key=settings.GROQ_API_KEY)

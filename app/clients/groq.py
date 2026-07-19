from groq import AsyncGroq

from app.core.config import get_settings

settings = get_settings()

client = AsyncGroq(api_key=settings.GROQ_API_KEY)


def get_groq_client() -> AsyncGroq:
    return client

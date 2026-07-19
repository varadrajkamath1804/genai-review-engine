from groq import AsyncGroq
from fastapi import Request

from app.core.config import get_settings

settings = get_settings()

client = AsyncGroq(api_key="dummy")


def create_groq_client() -> AsyncGroq:
    return AsyncGroq(api_key=settings.GROQ_API_KEY)


def get_groq_client(request: Request) -> AsyncGroq:
    return request.app.state.groq

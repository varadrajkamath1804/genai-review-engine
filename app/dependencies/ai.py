from fastapi import Depends
from openai import AsyncOpenAI

from app.clients.openai import get_openai_client
from app.services.ai_service import AIService


def get_ai_service(client: AsyncOpenAI = Depends(get_openai_client)) -> AIService:
    return AIService(client)

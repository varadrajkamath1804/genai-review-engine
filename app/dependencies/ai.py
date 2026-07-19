from fastapi import Depends
from groq import AsyncGroq

from app.clients.groq import get_groq_client
from app.services.ai_service import AIService


def get_ai_service(client: AsyncGroq = Depends(get_groq_client)) -> AIService:
    return AIService(client)

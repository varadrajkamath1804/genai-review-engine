from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from groq import AsyncGroq

from app.clients.groq import create_groq_client
from app.models.review import ReviewInput
from app.models.sentiment import SentimentResponse
from app.services.ai_service import AIService
from app.dependencies.ai import get_ai_service
from app.core.database import engine
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.groq = create_groq_client()
    print("Groq Client created")
    yield
    await app.state.groq.close()
    print("Groq Client closed")


app = FastAPI(lifespan=lifespan)


@app.post("/analyze")
async def analyze_review(
    review: ReviewInput, ai_service: AIService = Depends(get_ai_service)
) -> SentimentResponse:

    return await ai_service.analyze_review(review)


@app.get("/db/health")
async def database_health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"status": "connected"}
